package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import paradot.mobilzeo.entity.MobilePlanViewEntity

interface ItemViwCountData {
    var itemId: String
    var viewCount: String
}

interface MobilePlanViewRepository : JpaRepository<MobilePlanViewEntity, Int> {
    @Query(
        "select mobile_plan_id as itemId, count(*) as viewCount from mobile_plan_view \n" +
                "group by mobile_plan_id",
        nativeQuery = true
    )
    fun getMobilePlanViewCountData(): List<ItemViwCountData>
}