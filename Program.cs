using System;

namespace SimpleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Welcome to SimpleApp!");
            Console.WriteLine("======================");

            Calculator calc = new Calculator();

            int a = 10;
            int b = 5;

            Console.WriteLine($"\nCalculating with numbers: {a} and {b}");
            Console.WriteLine($"Addition: {calc.Add(a, b)}");
            Console.WriteLine($"Subtraction: {calc.Subtract(a, b)}");
            Console.WriteLine($"Multiplication: {calc.Multiply(a, b)}");
            Console.WriteLine($"Division: {calc.Divide(a, b)}");

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
