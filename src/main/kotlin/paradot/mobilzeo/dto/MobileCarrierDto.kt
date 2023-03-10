package paradot.mobilzeo.dto

class MobileCarrierDto(
    val id: Int,
    val thumbnail_url: String,
    val name: String,
    val support_skt: Boolean,
    val support_kt: Boolean,
    val support_lg: Boolean,
    val business_hour_title: String,
    val business_hour_subtitle: String,
    val customer_service: String,
    val location: String
)