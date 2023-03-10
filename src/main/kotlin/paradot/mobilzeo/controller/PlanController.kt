package paradot.mobilzeo.controller

import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller

@Controller
class PlanController {
    @QueryMapping
    fun mobilePlans(): List<String> {
        return listOf("dd", "aa")
    }

//    @SchemaMapping
//    fun releases(project: Project): List<Release> {
//        return client.fetchProjectReleases(project.getSlug())
//    }
}