package paradot.mobilzeo.service

import org.springframework.stereotype.Service
import paradot.mobilzeo.repository.MobileCarrierRepository
import paradot.mobilzeo.repository.MobilePlanRepository

@Service
class PlanService(
    private val mobilePlanRepository: MobilePlanRepository,
    private val mobileCarrierRepository: MobileCarrierRepository
) {


}