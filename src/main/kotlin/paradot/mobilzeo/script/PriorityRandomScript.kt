package paradot.mobilzeo.script

import paradot.mobilzeo.repository.MobilePlanRepository
import java.util.Random

class PriorityRandomScript(private val mobilePlanRepository: MobilePlanRepository) {
    fun random() {
        val allPlans = mobilePlanRepository.findAll()
        allPlans.forEach { plan ->
            plan.priority = if (plan.youtubeUrl == null) {
                Random().nextInt(0, 70)
            } else {
                Random().nextInt(40, 80)
            }

            mobilePlanRepository.save(plan)
        }
    }
}