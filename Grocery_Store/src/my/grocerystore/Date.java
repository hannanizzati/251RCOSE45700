/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package my.grocerystore;

/**
 *
 * @author dinie
 */
public class Date {
    //data fields
    protected int day, month, year;

    //no arguments constructor
    protected Date() {
        day=0;
        month=0;
        year=0;
    }
    // constructor with arg
    protected Date(int day, int month, int year) {
        this.day = day;
        this.month=month;
        this.year=year;
    }
    //accessors and mutators
    public int getDay() {
        return day;
    }
    public int getMonth() {
        return month;
    }
    public int getYear() {
        return year;
    }
    public void setDay(int day) {
        this.day = day;
    }
    public void setMonth(int month) {
        this.month = month;
    }
    public void setYear(int year) {
        this.year = year;
    }
    //method
    protected String displayDate(){
        return day + "/" + month + "/" + year;
    }
}//end class
