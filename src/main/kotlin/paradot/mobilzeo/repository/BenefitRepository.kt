package paradot.mobilzeo.repository

import org.springframework.data.jpa.repository.JpaRepository
import paradot.mobilzeo.entity.BenefitEntity

interface BenefitRepository : JpaRepository<BenefitEntity, Int>