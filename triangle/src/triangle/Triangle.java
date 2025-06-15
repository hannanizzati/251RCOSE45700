/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package triangle;


/**
 *
 * @author Miit
 */
import java.util.*;
public class Triangle {
    //declare the main method
    public static void main (String [] args)
    {
        //scanner class - for input
        Scanner scanner = new Scanner(System.in);
        
        //declare variable to be use
        int base, height;
        double area;
        
        //prompt for base
        System.out.println("Pwidi please enter base :");
        
        //get base
        base = scanner.nextInt();
        
        //prompt for height
        System.out.println ("Pwidi please enter height:");
        
        //get height
        height = scanner.nextInt();
        
        //calculate the area
        area = 0.5*base*height;
        
        //display the area
        System.out.println ( "The area is: " +area);
        
    }//end of main
}//end of class


