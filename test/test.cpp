// sample C++ program to be executed by python file 'test.py'

#include <iostream>
#include <fstream>

using namespace std;

int main() {
    // initialize values to be read in
    int x;
    int y;
    // open stream, read data, set x and y, close stream
    ifstream in;
    in.open("input.txt");
    in >> x >> y;
    in.close();
    // perform operation with x and y
    int z;
    z = x + y;
    // open stream, write output of the operation to 'output.txt', close stream
    ofstream out;
    out.open("output.txt");
    out << z << " is the output" << endl;
    out.close();
    return 0;
}
