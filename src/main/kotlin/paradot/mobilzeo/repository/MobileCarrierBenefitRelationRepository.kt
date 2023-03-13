package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.MobileCarrierBenefitRelationEntity

interface MobileCarrierBenefitRelationRepository : JpaRepository<MobileCarrierBenefitRelationEntity, Int> {
    fun findAllByMobileCarrierId(mobileCarrierId: Int): List<MobileCarrierBenefitRelationEntity>
}