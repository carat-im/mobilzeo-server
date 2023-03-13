package paradot.mobilzeo.service

import org.springframework.data.repository.findByIdOrNull
import org.springframework.stereotype.Service
import paradot.mobilzeo.dto.MobilePlanDto
import paradot.mobilzeo.entity.MobilePlanViewEntity
import paradot.mobilzeo.repository.MobileCarrierRepository
import paradot.mobilzeo.repository.MobilePlanRepository
import paradot.mobilzeo.repository.MobilePlanViewRepository

@Service
class PlanService(
    private val mobilePlanRepository: MobilePlanRepository,
    private val mobileCarrierRepository: MobileCarrierRepository,
    private val mobilePlanViewRepository: MobilePlanViewRepository,
) {

    fun getMobilePlans(): List<MobilePlanDto> {
        val allCarrierIds = mobilePlanRepository.findAllCarrierIds()
        val allCarrierDtoList = mobileCarrierRepository.findAllById(allCarrierIds).map { it.toMobileCarrierDto() }
        val allViewCountData = mobilePlanViewRepository.getMobilePlanViewCountData()

        return mobilePlanRepository.findAll()
            .mapNotNull {
                val mobileCarrierDto =
                    allCarrierDtoList.firstOrNull { mobileCarrierDto -> mobileCarrierDto.id == it.mobileCarrierId }

                val mobilePlanDto = it.toMobilePlanDto(mobileCarrierDto)
                    ?: return@mapNotNull null

                mobilePlanDto.view_count =
                    allViewCountData.firstOrNull { data -> data.itemId.toInt() == mobilePlanDto.id }?.viewCount?.toInt() ?: 0
                mobilePlanDto
            }
    }

    fun getMobilePlan(planId: Int): MobilePlanDto? {
        val planEntity = mobilePlanRepository.findByIdOrNull(planId)
            ?: return null
        val carrierDto = mobileCarrierRepository.findByIdOrNull(planEntity.mobileCarrierId)?.toMobileCarrierDto()
            ?: return null

        return planEntity.toMobilePlanDto(carrierDto)
    }

    fun saveViewForMobilePlan(planId: Int): Int {
        val viewEntity = MobilePlanViewEntity(planId)
        val savedViewEntity = mobilePlanViewRepository.save(viewEntity)

        return savedViewEntity.id
    }
}