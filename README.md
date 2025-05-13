# 🌿 AI Royal Virus (Nature Wars)

**AI Royal Virus** is a strategic tile-based game built using **Python and Pygame**, where the player competes against an intelligent AI to dominate a nature-themed grid. Navigate through tiles representing the elements — Water, Air, Earth, and Fire — and be the first to reach **35 points** or secure control of high-value nature tiles.

![Nature Wars Preview](https://via.placeholder.com/600x400.png?text=Game+Preview) <!-- You can replace this with a real screenshot -->

---

## 🎮 Gameplay Overview

- **Grid Size:** 8x8
- **Goal:** Reach 35 points or control all high-value tiles (Air 💨, Water 💧)
- **Turns:** Player and AI alternate moves
- **Movement:** Step into adjacent (up/down/left/right) empty tiles
- **Points System:**
  - 💧 Water: +3 points
  - 🌬️ Air: +5 points
  - ⬜ Neutral: +1 point
  - 🌍 Earth: -3 points
  - 🔥 Fire: -5 points

---

## 🧠 AI Features

The AI uses a **minimax algorithm with alpha-beta pruning** and prioritizes:
- High-value tile acquisition
- Restricting player movement
- Strategic trap placement

---

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-royal-virus.git
   cd ai-royal-virus
2. **Install dependencies**:
   pip install pygame numpy
3. **Run the game**:
   python "AI Royal Virus.py"


**📋 Rules Summary**
- Move to adjacent tiles to gain control
- Each tile gives or subtracts points based on its type
- Game ends when:
  - A player reaches 35 points
  - No positive tiles remain
  - All tiles are filled
  - No valid moves left

**How to Play**
1) Read the rules when the game starts
2) Click on adjacent empty tiles to make your move
3) Try to capture Water and Air tiles for maximum points
4) Avoid Fire and Earth tiles when possible
5) Reach 35 points before the AI does!

**✨ Features**
- Colorful and emoji-rich UI for an engaging experience
- AI with strategic depth
- Easy-to-read rules screen
- Win screen with dynamic messages

**Technical Details**
- Board Size: 8x8 grid
- AI Algorithm: Minimax with alpha-beta pruning (depth 5)
- Evaluation Function: Considers:
   - Score difference
   - Available moves
   - Control of high-value tiles
   - Player trapping opportunitie

**🧑‍💻 Author**
- Muhammad Hamiz Siddiqui
- Zuhair Zeshan
  
Feel free to reach out or contribute!

**License**
This project is open-source and available under the MIT License.


