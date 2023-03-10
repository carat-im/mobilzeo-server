package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import paradot.mobilzeo.entity.MobilePlanEntity

interface MobilePlanRepository : JpaRepository<MobilePlanEntity, Int> {
    @Query("select distinct mobile_carrier_id from mobile_plan", nativeQuery = true)
    fun findAllCarrierIds(): List<Int>
}