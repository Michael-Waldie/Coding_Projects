package Final;

// The purpose of this class is to create a ledger based off of an income and expense for each month.
// Michael Waldie 8/8/2021

import javax.swing.JOptionPane; // Needed for the dialog boxed
import java.util.Scanner;       // Needed to access files.
import java.io.*;               // Needed for the File class

public class IncomeLedger {

	public double[] savings = new double[12];     // An array that stores the savings for each month (negative implies a loss that month).
	public double value = 0;                      // Total savings for the year.
	public double[][] ledger = new double[2][12]; // A 2D array which first row of ledger contains monthly income (in USD).
	                                              // The second row contains monthly expense (in USD).       
	static String[] months = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}; // Array of months.
	
	// Constructor.
	// Sets up a ledger using input from the user.
	public IncomeLedger() throws FileNotFoundException, IOException {
		// Initialize the 1st row values of the ledger array from the income.txtfile.
		// Each line is its own month
		File file = new File("income.txt");
		Scanner inputFile = new Scanner(file);
		int count = 0;
		while(inputFile.hasNext()) {
			String nextLine = inputFile.next();
			ledger[0][count] = Double.parseDouble(nextLine);
			count++;
		}
		inputFile.close();
		
		// Initialize the 2nd row values of the ledger array from the keyboard input
		for(int i = 0;i < 12;i++) ledger[1][i] = Double.parseDouble(JOptionPane.showInputDialog("Enter expense " + (i+1) + ":").strip());
		
		// Calculate the savings of each month and the total value
		for(int i = 0;i < 12;i++) {
			savings[i] = ledger[0][i] - ledger[1][i];
			value += savings[i];
		}
	}
	
	// Used to generate a ledger to output.txt
	public static void main(String[] args) throws IOException {
		IncomeLedger l = new IncomeLedger(); // New Ledger object.
		Calculator c = new Calculator(l);    // New Calculator object.
		c.average();                         // Gets average savings.
		c.maxValue();                        // Gets maximum savings of the ledger.
		c.minValue();                        // Gets minimum savings of the ledger.
		c.sortValue();                       // Sorts the savings array.
		
		// Create a file called output.txt.
		File output = new File("output.txt");
		
		// Print/save the following information in the output.txt.
		PrintWriter outputFile = new PrintWriter(output);
		// Monthly income in USD – Month names and amounts
		outputFile.println("Monthly Income");
		outputFile.println("-------------------------");
		for(int i=0;i<12;i++) {
			outputFile.printf("%s: %.2f USD\n", months[i], l.ledger[0][i]);
		}
		outputFile.println();
		// Monthly expense in USD – month names and amounts
		outputFile.println("Monthly Expense");
		outputFile.println("-------------------------");
		for(int i=0;i<12;i++) {
			outputFile.printf("%s: %.2f USD\n", months[i], l.ledger[1][i]);
		}
		outputFile.println();
		//Monthly Savings in USD – month names and amounts
		outputFile.println("Monthly Savings");
		outputFile.println("-------------------------");
		for(int i=0;i<12;i++) {
			outputFile.printf("%s: %.2f USD\n", months[i], l.savings[i]);
		}
		outputFile.println();
		// Average savings – month name and amount
		outputFile.printf("Average savings: %.2f USD\n", c.averageSavings);
		// Maximum savings – month name and amount
		outputFile.printf("Maximum savings: %.2f USD\n", c.maxVal);
		// Minimum savings – month name and amount
		outputFile.printf("Minimum savings: %.2f USD\n", c.minVal);
		outputFile.println();
		// Sorted savings in descending order – month names and amounts
		outputFile.println("Sorted Savings");
		outputFile.println("-------------------------");
		for(int i=0;i<12;i++) {
			outputFile.printf("%s: %.2f USD\n", c.sortMonths[i], c.sortSavings[i]);
		}
		outputFile.close();
	}
}
