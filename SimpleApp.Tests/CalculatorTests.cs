using System;
using NUnit.Framework;

namespace SimpleApp.Tests
{
    [TestFixture]
    public class CalculatorTests
    {
        private Calculator _calculator;

        [SetUp]
        public void SetUp()
        {
            _calculator = new Calculator();
        }

        [TestCase(2, 3, 5)]
        [TestCase(-1, -2, -3)]
        [TestCase(-1, 3, 2)]
        [TestCase(0, 5, 5)]
        [TestCase(5, 0, 5)]
        [TestCase(0, 0, 0)]
        [TestCase(100, 100, 200)]
        public void Add_ReturnsCorrectResult(int a, int b, int expected)
        {
            int result = _calculator.Add(a, b);

            Assert.That(result, Is.EqualTo(expected));
        }

        [TestCase(int.MaxValue, 1)]
        [TestCase(int.MinValue, -1)]
        public void Add_Overflow_WrapsAround(int a, int b)
        {
            int result = _calculator.Add(a, b);

            unchecked
            {
                Assert.That(result, Is.EqualTo(unchecked(a + b)));
            }
        }

        [TestCase(5, 3, 2)]
        [TestCase(-1, -2, 1)]
        [TestCase(-1, 3, -4)]
        [TestCase(0, 5, -5)]
        [TestCase(5, 0, 5)]
        [TestCase(0, 0, 0)]
        [TestCase(5, 5, 0)]
        public void Subtract_ReturnsCorrectResult(int a, int b, int expected)
        {
            int result = _calculator.Subtract(a, b);

            Assert.That(result, Is.EqualTo(expected));
        }

        [TestCase(int.MinValue, 1)]
        [TestCase(int.MaxValue, -1)]
        public void Subtract_Overflow_WrapsAround(int a, int b)
        {
            int result = _calculator.Subtract(a, b);

            unchecked
            {
                Assert.That(result, Is.EqualTo(unchecked(a - b)));
            }
        }

        [TestCase(2, 3, 6)]
        [TestCase(-2, -3, 6)]
        [TestCase(-2, 3, -6)]
        [TestCase(0, 5, 0)]
        [TestCase(5, 0, 0)]
        [TestCase(5, 5, 25)]
        [TestCase(1, int.MaxValue, int.MaxValue)]
        public void Multiply_ReturnsCorrectResult(int a, int b, int expected)
        {
            int result = _calculator.Multiply(a, b);

            Assert.That(result, Is.EqualTo(expected));
        }

        [TestCase(int.MaxValue, 2)]
        [TestCase(int.MinValue, 2)]
        public void Multiply_Overflow_WrapsAround(int a, int b)
        {
            int result = _calculator.Multiply(a, b);

            unchecked
            {
                Assert.That(result, Is.EqualTo(unchecked(a * b)));
            }
        }

        [TestCase(10, 2, 5.0)]
        [TestCase(7, 2, 3.5)]
        [TestCase(-10, 2, -5.0)]
        [TestCase(10, -2, -5.0)]
        [TestCase(-10, -2, 5.0)]
        [TestCase(0, 5, 0.0)]
        public void Divide_ReturnsCorrectResult(int a, int b, double expected)
        {
            double result = _calculator.Divide(a, b);

            Assert.That(result, Is.EqualTo(expected).Within(1e-10));
        }

        [TestCase(int.MaxValue, 1, (double)int.MaxValue)]
        [TestCase(int.MinValue, 1, (double)int.MinValue)]
        [TestCase(int.MaxValue, -1, -(double)int.MaxValue)]
        [TestCase(int.MinValue, -1, -(double)int.MinValue)]
        public void Divide_BoundaryValues_ReturnsCorrectResult(int a, int b, double expected)
        {
            double result = _calculator.Divide(a, b);

            Assert.That(result, Is.EqualTo(expected).Within(1e-10));
        }

        [Test]
        public void Divide_RepeatingDecimal_ReturnsCorrectResult()
        {
            double result = _calculator.Divide(1, 3);

            Assert.That(result, Is.EqualTo(1.0 / 3.0).Within(1e-10));
        }

        [TestCase(1, 0)]
        [TestCase(0, 0)]
        [TestCase(-1, 0)]
        public void Divide_ByZero_ThrowsDivideByZeroException(int a, int b)
        {
            var ex = Assert.Throws<DivideByZeroException>(() => _calculator.Divide(a, b));

            Assert.That(ex.Message, Is.EqualTo("Cannot divide by zero."));
        }

        [Test]
        public void Divide_SameValue_ReturnsOne()
        {
            double result = _calculator.Divide(5, 5);

            Assert.That(result, Is.EqualTo(1.0).Within(1e-10));
        }
    }
}
