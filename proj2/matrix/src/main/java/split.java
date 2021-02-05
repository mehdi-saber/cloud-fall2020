import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Random;
import java.util.Scanner;

public class split {
    public static void main(String[] args) throws FileNotFoundException {
        FileInputStream fi = new FileInputStream("test.txt");
        Scanner in = new Scanner(fi);


        for (int i = 0; in.hasNext(); i++) {
            FileOutputStream fs = new FileOutputStream("test/test"+i);
            PrintStream out = new PrintStream(fs);
            for (int j = 0; j < 10000&&in.hasNext(); j++) {
                out.println(in.nextLine());
            }
            out.close();
        }
        in.close();
    }
}
