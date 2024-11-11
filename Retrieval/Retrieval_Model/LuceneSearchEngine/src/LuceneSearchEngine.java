import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;

import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Objects;

public class LuceneSearchEngine {
    // Variables
    private static Analyzer analyzer = new SimpleAnalyzer();
    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<>();

    /**
     * Constructor
     *
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    private LuceneSearchEngine(String indexDir) throws IOException {

        FSDirectory dir = FSDirectory.open(new File(indexDir).toPath());
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        writer = new IndexWriter(dir, config);

    }

    /**
     * Indexes a file or directory
     *
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();
        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", fr));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(),
                        Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out
                .println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
    }

    /**
     * add files to the queue to be processed.
     *
     * @param file: filename or directory name to be added
     */
    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : Objects.requireNonNull(file.listFiles())) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html")
                    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
        writer.close();
    }

    public static void main(String[] args) throws IOException{

        String indexLocation = null;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = "";

        LuceneSearchEngine indexer = null;
        try {

            Path p = Paths.get(".","Index", "Index");
            s = p.toString();
            indexLocation = s;
            indexer = new LuceneSearchEngine(s);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }

        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        int m = 1;
        while (m++ <= 1) {
            try {

            	
               
                Path p =  Paths.get("..", "..","..","utilities", "Material\\cacm.tar");
                s = p.toString();


                // try to add file into the index
                indexer.indexFileOrDirectory(s);
            } catch (Exception e) {
                System.out.println("Error indexing " + s + " : "
                        + e.getMessage());
            }
        }

        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search
        // =========================================================
        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
                indexLocation).toPath()));
        IndexSearcher searcher = new IndexSearcher(reader);


        s = "";
        int counter = 1;
        try {
        	
            File file = new File("..\\..\\..\\utilities\\queries.txt");
        	
            FileReader fileReader = new FileReader(file);
            BufferedReader bufferedReader = new BufferedReader(fileReader);

            PrintWriter printWriter = null;
            FileWriter fileWriter = null;

            fileWriter = new FileWriter("results.txt");
            printWriter = new PrintWriter(fileWriter);
            int qnum =0;
            while ((s = bufferedReader.readLine()) != null) {
            	qnum=qnum+1;
            	 Query q = new QueryParser("contents",
                         analyzer).parse(QueryParser.escape(s));
                TopScoreDocCollector collector = TopScoreDocCollector.create(100);
                searcher.search(q, collector);
                ScoreDoc[] hits = collector.topDocs().scoreDocs;

                // 4. printing result
                System.out.println("Found " + hits.length + " hits.");
                
                for (int i = 0; i < hits.length; ++i) {
                    int docId = hits[i].doc;
                    Document d = searcher.doc(docId);
                    String n = d.get("path");
                    Path p = Paths.get(n);
                    n = p.getFileName().toString();
                    n = n.substring(0, n.lastIndexOf('.'));

                    //printWriter.print(String.format("%d. %-40s %s \r\n", i + 1, n, hits[i].score));
                    printWriter.print(qnum+"\tQ0\t"+n+"\t"+(i+1)+"\t"+hits[i].score+"\t"+"Lucene_BM25_regular_corpus"+"\n");
                }

                System.out.println("Results produced for query: " + counter);
                counter++;
            }
            printWriter.close();
            fileWriter.close();

        } catch (Exception e) {
            System.out.println("Error searching " + s + " : "
                    + e.getMessage());
        }
    }

}
