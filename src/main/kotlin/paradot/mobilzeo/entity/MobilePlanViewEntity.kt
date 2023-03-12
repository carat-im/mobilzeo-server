package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import java.time.LocalDateTime

@Entity(name = "mobile_plan_view")
class MobilePlanViewEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    @Column(name = "mobile_plan_id")
    var mobilePlanId: Int = -1

    @Column(name = "view_at")
    var viewAt: LocalDateTime = LocalDateTime.now()

    constructor()

    constructor(mobilePlanId: Int) : this() {
        this.mobilePlanId = mobilePlanId
    }
}