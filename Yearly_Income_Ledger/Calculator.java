package Final;

// The purpose of this class is to do some calculations based on values in ledger
// Michael Waldie 8/8/2021

import java.io.IOException;
import java.util.Arrays; // Needed for several Arrays methods

public class Calculator {
	
	public IncomeLedger l;                       // An IncomeLedger object to get the savings values from
	public double averageSavings;                // Average savings of a ledger
	public double maxVal;                        // The maximum value of savings in a ledger
	public int maxMonth;                         // The month of which the maximum savings was in
	public double minVal;                        // The minimum value of savings in a ledger
	public int minMonth;                         // The minimum of which the maximum savings was in
	public double[] sortSavings;                 // Savings from each month sorted from highest to lowest value
	public String[] sortMonths = new String[12]; // Month sorted based on sortSavings
	
	// Constructor.
	// Sets variables for a calculator to their base value
	public Calculator(IncomeLedger ledger) throws IOException {
		l = ledger;
		averageSavings = 0;
		maxVal = 0;
		minVal = 0;
		maxMonth = 0;
		minMonth = 0;
		sortSavings = Arrays.copyOf(l.savings, 12);
	}
	
	// The average method calculates the average savings in a ledger and stores it in averageSavings.
	public void average() {
		averageSavings = l.value/12;
	}
	
	// The maxValue method finds the maximum savings value and stores it in maxVal.
	// It also stores the month of this value in maxMonth.
	public  void maxValue() {
		double max = l.savings[0];
		int month = 0;
		for(int i=0;i<l.savings.length;i++) {
			if(l.savings[i]>max) {  // If a larger value is found:
				max = l.savings[i]; // Store the value in current max and month.
				month = i;
			}
		}
		maxVal = max; // Set the final min and month.
		maxMonth = month;
	}
	
	// The minValue method finds the minimum savings value and stores it in minVal.
	// It also stores the month of this value in minMonth.
	public  void minValue() {
		double min = l.savings[0];
		int month = 0;
		for(int i=0;i<l.savings.length;i++) {
			if(l.savings[i]<min) {  // If a smaller value is found:
				min = l.savings[i]; // Store the value in current min and month.
				month = i;
			}
		}
		minVal = min; // Set the final min and month.
		minMonth = month;
	}	
	
	// The sortValue method organizes the savings array from a ledger from greatest to least and stores it in sortSavings.
	// It also stores the organized months of sortSavings based on their values.
	public void sortValue() {
		for(int i=0;i<sortSavings.length;i++) {
			for(int j=0;j<sortSavings.length;j++) {
				double temp = 0;
				if(sortSavings[i]>sortSavings[j]) {  // If a greater value is found:
					temp = sortSavings[i];           // (Temporary spot to hold next biggest value.)
					sortSavings[i] = sortSavings[j]; // Switch the values of i with j
					sortSavings[j] = temp;
					}
				}
			}
		// Stores months into SortMonths based off of sortSavings.
		for(int i = 0;i<sortSavings.length;i++) {
			for(int j = 0;j<sortSavings.length;j++) {
				if(sortSavings[i] == l.savings[j]) {                     // If a match is found store it in sortMonths if:
					if (Arrays.asList(sortMonths).contains("" + (j+1))); // j is not already in sortMonths
					else sortMonths[i] = "" + (j+1);
				}
			}
		}
		// Switches the months to string format instead of integer format.
		for(int x=0;x<12;x++) {
			switch(Integer.parseInt(sortMonths[x])) {
			case 1: sortMonths[x] = "Jan";
			break;
			case 2: sortMonths[x] = "Fed";
			break;
			case 3: sortMonths[x] = "Mar";
			break;
			case 4: sortMonths[x] = "Apr";
			break;
			case 5: sortMonths[x] = "May";
			break;
			case 6: sortMonths[x] = "Jun";
			break;
			case 7: sortMonths[x] = "Jul";
			break;
			case 8: sortMonths[x] = "Aug";
			break;
			case 9: sortMonths[x] = "Sep";
			break;
			case 10: sortMonths[x] = "Oct";
			break;
			case 11: sortMonths[x] = "Nov";
			break;
			case 12: sortMonths[x] = "Dec";
			break;
			}
		}
	}
}