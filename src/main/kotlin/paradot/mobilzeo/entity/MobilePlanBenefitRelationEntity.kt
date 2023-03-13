package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity(name = "mobile_plan_benefit_relation")
class MobilePlanBenefitRelationEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    @Column(name = "mobile_plan_id")
    var mobilePlanId: Int = -1

    @Column(name = "benefit_id")
    var benefitId: Int = -1
}