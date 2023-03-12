package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.MobilePlanViewEntity

interface MobilePlanViewRepository : JpaRepository<MobilePlanViewEntity, Int>