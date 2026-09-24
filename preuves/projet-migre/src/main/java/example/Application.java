package example;

import tools.jackson.databind.ObjectMapper;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class Application {
    public static void main(String[] args) { SpringApplication.run(Application.class, args); }
}

@Entity
class Person {
    @Id public Long id;
    public String name;
}

interface PersonRepository extends JpaRepository<Person, Long> {}

@RestController
class Controller {
    private final ObjectMapper mapper;
    Controller(ObjectMapper mapper) { this.mapper = mapper; }
    @GetMapping("/hello")
    String hello() { return mapper.writeValueAsString("hello"); }
}
