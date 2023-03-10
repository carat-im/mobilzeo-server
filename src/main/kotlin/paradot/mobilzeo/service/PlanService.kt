package paradot.mobilzeo.service

import org.springframework.data.repository.findByIdOrNull
import org.springframework.stereotype.Service
import paradot.mobilzeo.dto.MobilePlanDto
import paradot.mobilzeo.repository.MobileCarrierRepository
import paradot.mobilzeo.repository.MobilePlanRepository

@Service
class PlanService(
    private val mobilePlanRepository: MobilePlanRepository,
    private val mobileCarrierRepository: MobileCarrierRepository
) {

    fun getMobilePlans(): List<MobilePlanDto> {
        val allCarrierIds = mobilePlanRepository.findAllCarrierIds()
        val allCarrierDtoList = mobileCarrierRepository.findAllById(allCarrierIds).map { it.toMobileCarrierDto() }

        return mobilePlanRepository.findAll()
            .mapNotNull {
                val mobileCarrierDto =
                    allCarrierDtoList.firstOrNull { mobileCarrierDto -> mobileCarrierDto.id == it.mobileCarrierId }
                it.toMobilePlanDto(mobileCarrierDto)
            }
    }

    fun getMobilePlan(planId: Int): MobilePlanDto? {
        val planEntity = mobilePlanRepository.findByIdOrNull(planId)
            ?: return null
        val carrierDto = mobileCarrierRepository.findByIdOrNull(planEntity.mobileCarrierId)?.toMobileCarrierDto()
            ?: return null

        return planEntity.toMobilePlanDto(carrierDto)
    }
}