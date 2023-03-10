package paradot.mobilzeo.controller

import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.ResponseBody

@Controller
@RequestMapping("/admin")
class AdminController {

    @GetMapping("/health")
    @ResponseBody
    fun getHealth(): String {
        return "healthy movn~"
    }
}