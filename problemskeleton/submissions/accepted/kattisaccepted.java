package problemskeleton.submissions.accepted;

import java.io.*;
import java.util.*;

public class kattisaccepted {
    public static void main(String[] args) throws IOException {

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in)); // Create line reader to parse Stdin.in
        List<String> bad = new ArrayList<>();
        int n = Integer.parseInt(br.readLine().trim());

        for (int k = 0; k < n; k++) { // For n lines in firewall
            String s = br.readLine().trim();

            long val = 0;
            boolean ok = true;

            for (int i = 1; i <= s.length(); i++) { // For each line, analyze all characters and check polydivisibility
                int digit = s.charAt(i - 1);
                val = val * 10 + Character.getNumericValue(digit); // Use same carry-forward logic as Python implementation using basic principles base 10 numbers

                if (val % i != 0) {
                    ok = false;
                    break;
                }
            }

            if (!ok) bad.add(s);
        }

        if (bad.isEmpty()) {
            System.out.println("Firewall is secure!");
        } else {
            System.out.println("Vulnerabilities detected:");
            for (String b : bad) System.out.println(b);
        }
    }
}