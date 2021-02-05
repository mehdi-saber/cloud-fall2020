import java.io.*;
import java.util.Random;

public class Gen {
    public static void main(String[] args) throws FileNotFoundException {
        Random random = new Random();
        FileOutputStream fs = new FileOutputStream("test.txt");
        PrintStream out = new PrintStream(fs);
        int m=10;
        int n=10;
        int p=10;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                int r_int = random.nextInt(100);
                out.printf("A[%d,%d]=%d\n", i,j,r_int);
            }
            System.out.println((int)(i/(float)m*100)+"%");
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < p; j++) {
                int r_int = random.nextInt(100);
                out.printf("B[%d,%d]=%d\n", i,j,r_int);
            }
            System.out.println((int)(i/(float)n*100)+"%");
        }
        out.close();
    }
}
