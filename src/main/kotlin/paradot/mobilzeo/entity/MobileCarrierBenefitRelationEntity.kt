package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity(name = "mobile_carrier_benefit_relation")
class MobileCarrierBenefitRelationEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)

    @Column(name = "mobile_carrier_id")
    var mobileCarrierId: Int = -1

    @Column(name = "benefit_id")
    var benefitId: Int = -1
}