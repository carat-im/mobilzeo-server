package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.MobilePlanEntity

interface MobilePlanRepository : JpaRepository<MobilePlanEntity, Int>