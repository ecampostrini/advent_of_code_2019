#include <iostream>
#include <chrono>

/*
 * Checks that a given number is monotone and that at least
 * two adjacent digits are the same
 */
bool is_valid(int n) {
  uint8_t count_same = 1;
  bool has_only_two = false;
  int prev = 10;
  while (n) {
    if (n % 10 > prev) return false;
    if (n % 10 != prev) {
      has_only_two = has_only_two || count_same == 2; 
      count_same = 1;
    } else {
      count_same++; 
    }
    prev = n % 10;
    n /= 10;
  }
  return has_only_two || count_same == 2;
}

int main() {
  
  auto start = std::chrono::high_resolution_clock::now();
  size_t count = 0;
  for (int i = 137683; i <= 596253; i++){
    if (is_valid(i)) {
      std::cout << i << std::endl;
      count++;
    }
  };
  auto stop = std::chrono::high_resolution_clock::now();
  std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() << " ms" << std::endl;
  std::cout << "Count: " << count << std::endl;
  return 0;
}
