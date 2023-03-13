package paradot.mobilzeo.service

import org.springframework.data.repository.findByIdOrNull
import org.springframework.stereotype.Service
import paradot.mobilzeo.dto.MobilePlanDto
import paradot.mobilzeo.entity.MobilePlanViewEntity
import paradot.mobilzeo.repository.*

@Service
class PlanService(
    private val mobilePlanRepository: MobilePlanRepository,
    private val mobileCarrierRepository: MobileCarrierRepository,
    private val mobilePlanViewRepository: MobilePlanViewRepository,
    private val mobileCarrierBenefitRelationRepository: MobileCarrierBenefitRelationRepository,

    private val benefitRepository: BenefitRepository,
) {

    fun getMobilePlans(): List<MobilePlanDto> {
        val allCarrierIds = mobilePlanRepository.findAllCarrierIds()
        val allCarrierDtoList = mobileCarrierRepository.findAllById(allCarrierIds).map { it.toMobileCarrierDto() }
        val allViewCountData = mobilePlanViewRepository.getMobilePlanViewCountData()
        val allBenefits = benefitRepository.findAll()
        val allBenefitRelations = mobileCarrierBenefitRelationRepository.findAll()

        return mobilePlanRepository.findAll()
            .mapNotNull { mobilePlanEntity ->
                val mobileCarrierDto =
                    allCarrierDtoList.firstOrNull { mobileCarrierDto -> mobileCarrierDto.id == mobilePlanEntity.mobileCarrierId }
                        ?: return@mapNotNull null

                val mobilePlanDto = mobilePlanEntity.toMobilePlanDto(mobileCarrierDto)
                    ?: return@mapNotNull null

                mobilePlanDto.view_count =
                    allViewCountData.firstOrNull { data -> data.itemId.toInt() == mobilePlanDto.id }?.viewCount?.toInt()
                        ?: 0

                val benefitIds =
                    allBenefitRelations.filter { relation -> relation.mobileCarrierId == mobileCarrierDto.id }
                        .map { it.benefitId }

                val benefitTitleList = allBenefits.filter { benefit -> benefit.id in benefitIds }.map { it.title }
                mobilePlanDto.banners = getBannerList(mobilePlanDto, benefitTitleList)
                mobilePlanDto
            }
    }

    fun getMobilePlan(planId: Int): MobilePlanDto? {
        val planEntity = mobilePlanRepository.findByIdOrNull(planId)
            ?: return null
        val carrierDto = mobileCarrierRepository.findByIdOrNull(planEntity.mobileCarrierId)?.toMobileCarrierDto()
            ?: return null

        val mobilePlanDto = planEntity.toMobilePlanDto(carrierDto)
            ?: return null

        val benefitIds =
            mobileCarrierBenefitRelationRepository.findAllByMobileCarrierId(carrierDto.id).map { it.benefitId }
        val benefitDtoList = benefitRepository.findAllById(benefitIds).map { it.toBenefitDto() }

        mobilePlanDto.benefit = benefitDtoList

        return mobilePlanDto
    }

    fun saveViewForMobilePlan(planId: Int): Int {
        val viewEntity = MobilePlanViewEntity(planId)
        val savedViewEntity = mobilePlanViewRepository.save(viewEntity)

        return savedViewEntity.id
    }

    private fun getBannerList(mobilePlanDto: MobilePlanDto, benefitTitleList: List<String>): MutableList<String> {
        val bannerList = mutableListOf<String>()

        if (mobilePlanDto.youtube_url != null) {
            bannerList.add("유튜브추천")
        }

        if (mobilePlanDto.usim_price == 0) {
            bannerList.add("유심무료")
        }

        bannerList.addAll(benefitTitleList)

        return bannerList
    }
}