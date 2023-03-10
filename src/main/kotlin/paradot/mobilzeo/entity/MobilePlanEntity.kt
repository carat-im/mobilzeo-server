package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id

@Entity(name = "mobile_plan")
class MobilePlanEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    var mobileCarrierId: Int = -1

    @Column(name = "price_initial")
    var priceInitial: Int = 0

    var name:String = ""
}