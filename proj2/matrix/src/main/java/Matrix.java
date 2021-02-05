import java.util.regex.Pattern;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.util.regex.Matcher;
import org.apache.hadoop.mapreduce.*;
import java.io.IOException;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import java.util.Iterator;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;

public class Matrix {
    final static int m=10;
    final static int n=10;
    final static int p=10;
    static class Reduce extends Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterable<Text> values, Context context)throws IOException, InterruptedException {
            String[] value;
            float a_ij;
            float b_jk;
            Iterator<Text> iter = values.iterator();
            int[] a=new int[n];
            int[] b=new int[n];
            float result = 0.0f;
            while (iter.hasNext()) {
                Text val = iter.next();
                value = val.toString().split(",");
                if (value[0].equals("A")) {
                    a[Integer.parseInt(value[1])]= Integer.parseInt(value[2]);
                } else if (value[0].equals("B")){
                    b[Integer.parseInt(value[1])]=Integer.parseInt(value[2]);
                }
            }
            for (int j = 0; j < n; j++)
                result =result+ a[j] * b[j];
            if (result != 0.0f) {
                context.write(null,
                        new Text(key.toString() + "," + result));
            }
        }
    }

    static class Map extends Mapper<LongWritable, Text, Text, Text> {
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            Pattern pattern = Pattern.compile("(.)\\[(\\d+)\\,(\\d+)\\]=(\\d+)");
            Matcher matcher = pattern.matcher(value.toString());
            matcher.find();
            String[] values = new String[4];
            for (int i = 1; i <= matcher.groupCount(); i++)
                values[i-1]=matcher.group(i);
            Text outKey = new Text();
            Text outVal = new Text();
            if (values[0].equals("A")) {
                for (int k = 0; k < p; k++) {
                    outKey.set(values[1] + "," + k);
                    outVal.set("A" + "," + values[2] + "," + values[3]);
                    context.write(outKey, outVal);
                }
            } else if(values[0].equals("B")){
                for (int i = 0; i < m; i++) {
                    outKey.set(i + "," + values[2]);
                    outVal.set("B," + values[1] + "," + values[3]);
                    context.write(outKey, outVal);
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "multi");
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(Map.class);
        job.setOutputKeyClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        job.setJarByClass(Matrix.class);
        job.setReducerClass(Reduce.class);
        job.setOutputValueClass(Text.class);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}