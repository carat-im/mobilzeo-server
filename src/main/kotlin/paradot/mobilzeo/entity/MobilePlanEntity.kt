package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import paradot.mobilzeo.dto.MobileCarrierDto
import paradot.mobilzeo.dto.MobilePlanDto

@Entity(name = "mobile_plan")
class MobilePlanEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    var mobileCarrierId: Int = -1

    @Column(name = "price_initial")
    var priceInitial: Int = 0

    @Column(name = "price_after_change")
    var priceAfterChange: Int? = null

    @Column(name = "initial_price_month")
    var initialPriceMonth: Int? = null

    @Column(name = "data_per_month")
    var dataPerMonth: Int = 0

    @Column(name = "data_per_day")
    var dataPerDay: Int? = null

    @Column(name = "data_exhaustion_speed")
    var dataExhaustionSpeed: Double? = null

    @Column(name = "call_minutes")
    var callMinutes: Int = 0

    @Column(name = "text_messages")
    var textMessages: Int = 0

    @Column(name = "main_carrier")
    var mainCarrier: String = ""

    @Column(name = "")
    var usimSubtitle: String = ""

    @Column(name = "usim_title")
    var usimTitle: String = ""

    @Column(name = "usim_description")
    var usimDescription: String? = null

    @Column(name = "youtube_url")
    var youtubeUrl: String? = null

    @Column(name = "banner_list")
    var bannerList: String = ""

    @Column(name = "cta_url")
    var ctaUrl: String = ""

    @Column(name = "ars_call_minutes")
    var arsCallMinutes: Int? = null

    @Column(name = "usim_price")
    var usimPrice: Int = 0

    @Column(name = "usim_nfc_price")
    var usimNfcPrice: Int? = null

    @Column(name = "esim_price")
    var esimPrice: Int? = null

    @Column(name = "carrier_app")
    var carrierApp: String? = null

    @Column(name = "hotspot_giga")
    var hotspotGiga: Int? = null

    @Column(name = "micropayments_months")
    var micropaymentsMonths: Int? = null

    @Column(name = "roaming_minutes")
    var roamingMinutes: Int? = null

    @Column(name = "internet_iptv")
    var internetIptv: String? = null

    @Column(name = "family_complimentary")
    var familyComplimentary: String? = null

    @Column(name = "data_sharing")
    var dataSharing: String? = null

    @Column(name = "signup_auth")
    var signupAuth: String? = null

    @Column(name = "signup_minors")
    var signupMinors: String? = null

    @Column(name = "signup_foreigners")
    var signupForeigners: String? = null

    @Column(name = "plan_exceed")
    var planExceed: String = ""

    var name: String = ""

    fun toMobilePlanDto(carrierDto: MobileCarrierDto?): MobilePlanDto? {
        if (carrierDto == null) {
            return null
        }

        return MobilePlanDto(
            id = id,
            name = name,
            price_initial = priceInitial,
            price_after_change = priceAfterChange,
            initial_price_month = initialPriceMonth,
            data_per_month = dataPerMonth,
            data_per_day = dataPerDay,
            data_exhaustion_speed = dataExhaustionSpeed,
            call_minutes = callMinutes,
            text_messages = textMessages,
            main_carrier = mainCarrier,
            banners = listOf(),
            view_count = 0,
            usim_price = usimPrice,
            usim_nfc_price = usimNfcPrice,
            esim_price = esimPrice,
            usim_subtitle = usimSubtitle,
            usim_title = usimTitle,
            usim_description = usimDescription,
            benefit = listOf(),
            youtube_url = youtubeUrl,
            ars_call_minutes = arsCallMinutes,
            carrier_app = carrierApp,
            hotspot_giga = hotspotGiga,
            micropayments_months = micropaymentsMonths,
            roaming_minutes = roamingMinutes,
            internet_iptv = internetIptv,
            family_complimentary = familyComplimentary,
            data_sharing = dataSharing,
            priority = 0,
            signup_auth = signupAuth,
            signup_minors = signupMinors,
            signup_foreigners = signupForeigners,
            plan_exceed = planExceed,
            carrier = carrierDto,
            cta_url = ctaUrl
        )
    }
}