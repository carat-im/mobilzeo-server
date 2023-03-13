package paradot.mobilzeo.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import paradot.mobilzeo.dto.BenefitDto

@Entity(name = "benefit")
class BenefitEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int = -1

    @Column(name = "thumbnail_url")
    var thumbnailUrl: String = ""

    var title: String = ""

    var subtitle: String = ""

    @Column(name = "subtitle_cancel")
    var subtitleCancel: Boolean = false

    @Column(name = "subtitle_question")
    var subtitleQuestion: String? = null

    fun toBenefitDto(): BenefitDto {
        return BenefitDto(
            thumbnail_url = thumbnailUrl,
            title = title,
            subtitle = subtitle,
            subtitle_cancel = subtitleCancel,
            subtitle_question = subtitleQuestion
        )
    }
}