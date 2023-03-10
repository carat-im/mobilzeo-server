package paradot.mobilzeo.controller

import org.springframework.graphql.data.method.annotation.Argument
import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller
import paradot.mobilzeo.dto.MobilePlanDto
import paradot.mobilzeo.service.PlanService

@Controller
class PlanController(private val planService: PlanService) {
    @QueryMapping
    fun mobilePlans(): List<MobilePlanDto> {
        return planService.getMobilePlans()
    }

    @QueryMapping
    fun mobilePlan(@Argument id: Int): MobilePlanDto? {
        return planService.getMobilePlan(id)
    }
}