package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import paradot.mobilzeo.dto.MobileCarrierDto

@Entity(name = "mobile_carrier")
class MobileCarrierEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    var name: String = ""

    @Column(name = "thumbnail_url")
    var thumbnailUrl: String = ""

    @Column(name = "support_skt")
    var supportSkt: Boolean = false

    @Column(name = "support_kt")
    var supportKt: Boolean = false

    @Column(name = "support_lg")
    var supportLg: Boolean = false

    @Column(name = "business_hour_title")
    var businessHourTitle: String = ""

    @Column(name = "business_hour_subtitle")
    var businessHourSubtitle: String = ""

    @Column(name = "customer_service")
    var customerService: String = ""

    var location: String = ""

    fun toMobileCarrierDto(): MobileCarrierDto {
        return MobileCarrierDto(
            id = id,
            thumbnail_url = thumbnailUrl,
            name = name,
            support_skt = supportSkt,
            support_kt = supportKt,
            support_lg = supportLg,
            business_hour_title = businessHourTitle,
            business_hour_subtitle = businessHourSubtitle,
            customer_service = customerService,
            location = location
        )
    }
}
