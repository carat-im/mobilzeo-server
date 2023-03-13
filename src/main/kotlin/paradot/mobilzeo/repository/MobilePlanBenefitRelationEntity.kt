package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.MobilePlanBenefitRelationEntity

interface MobilePlanBenefitRelationRepository : JpaRepository<MobilePlanBenefitRelationEntity, Int> {
    fun findAllByMobilePlanId(mobilePlanId: Int): List<MobilePlanBenefitRelationEntity>
}