package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.MobileCarrierEntity

interface MobileCarrierRepository : JpaRepository<MobileCarrierEntity, Int>