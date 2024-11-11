import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

public class test {
    public static void main(String[] args){
        File s = new File("C:\\Users\\mohan\\Desktop\\Courses\\IR\\Course Project\\Project\\BFS_HTML_FILES\\Solar_eclipses_on_Mars.html");
        String n = "C:\\Users\\mohan\\Desktop\\Courses\\IR\\Course Project\\Project\\BFS_HTML_FILES\\Solar_eclipses_on_Mars.html";
        Path p = Paths.get(n);
        n = p.getFileName().toString();
//                s.toPath().getFileName().toString();
        n = n.substring(0, n.lastIndexOf('.'));
        System.out.println(n);
//        String[] p = n.split("\\\\");
//        p[p.length- 1])

    }
}
