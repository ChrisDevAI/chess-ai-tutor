import 'package:flutter/material.dart' as m;
import 'package:flutter_chess_board/flutter_chess_board.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

const String backendUrl = 'http://localhost:8000';

const m.Color darkBackground = m.Color(0xFF1E1E1E);
const m.Color panelBackground = m.Color(0xFF2C2C2C);
const m.Color goldAccent = m.Color(0xFFD9A066);
const m.Color woodBrown = m.Color(0xFF815B33);

void main() {
  m.runApp(const m.MaterialApp(home: ChessTutorScreen()));
}

class ChessTutorScreen extends m.StatefulWidget {
  const ChessTutorScreen({m.Key? key}) : super(key: key);

  @override
  m.State<ChessTutorScreen> createState() => _ChessTutorScreenState();
}

class _ChessTutorScreenState extends m.State<ChessTutorScreen> {
  final ChessBoardController _controller = ChessBoardController();

  String topMoves = "Calculating...";
  final chatController = m.TextEditingController();
  String chatResponse = "";

  List<String> moveHistory = [];
  int currentMoveIndex = 0;
  bool suppressMoveListener = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onMove);
  }

  List<String> _extractHalfMovesFromController() {
    final sanList = _controller.getSan().whereType<String>().toList();
    if (sanList.isEmpty) return [];

    final List<String> moves = [];
    for (final entry in sanList) {
      final parts = entry.split(RegExp(r'\s+'));
      for (final p in parts) {
        final token = p.trim();
        if (token.isEmpty) continue;
        if (RegExp(r'^\d+\.{1,3}$').hasMatch(token)) continue;
        moves.add(token);
      }
    }
    return moves;
  }

  void _onMove() async {
    if (suppressMoveListener) return;

    moveHistory = _extractHalfMovesFromController();
    currentMoveIndex = moveHistory.length;

    final fen = _controller.getFen();
    final result = await fetchBestMoves(fen);

    setState(() {
      topMoves = result;
    });
  }

  void _analyzePosition() async {
    final fen = _controller.getFen();
    final analysis = await analyzeFen(fen);
    setState(() => chatResponse = analysis);
  }

  void _sendChat() async {
    final message = chatController.text.trim();

    if (message.contains("1.") && message.contains(" ")) {
      final pgnResult = await loadPGN(message);
      if (pgnResult != null && pgnResult["pgn"] != null) {
        final pgn = pgnResult["pgn"];

        suppressMoveListener = true;
        _controller.resetBoard();
        _controller.loadPGN(pgn);
        suppressMoveListener = false;

        setState(() {
          moveHistory = _extractHalfMovesFromController();
          currentMoveIndex = moveHistory.length;
          topMoves = "";
          chatResponse = "";
        });

        chatController.clear();
        return;
      }
    }

    final fen = _controller.getFen();
    final reply = await chatWithLLM(message, fen);

    setState(() => chatResponse = reply);
    chatController.clear();
  }

  void goToMove(int index) {
    if (index < 0) index = 0;
    if (index > moveHistory.length) index = moveHistory.length;

    suppressMoveListener = true;
    _controller.resetBoard();

    if (index > 0) {
      final sanSequence = moveHistory.sublist(0, index).join(' ');
      _controller.loadPGN(sanSequence);
    }

    setState(() => currentMoveIndex = index);
    suppressMoveListener = false;
  }

  void goToStart() => goToMove(0);
  void goToPrev() => goToMove(currentMoveIndex - 1);
  void goToNext() => goToMove(currentMoveIndex + 1);
  void goToEnd() => goToMove(moveHistory.length);

  @override
  m.Widget build(m.BuildContext context) {
    final moveRows = (moveHistory.length + 1) ~/ 2;

    return m.Scaffold(
      backgroundColor: darkBackground,
      appBar: m.AppBar(
        backgroundColor: panelBackground,
        title: const m.Text("Chess AI Tutor",
            style: m.TextStyle(color: m.Colors.white)),
      ),
      body: m.Padding(
        padding: const m.EdgeInsets.all(8),
        child: m.Row(
          children: [
            _buildChatPanel(),
            m.Expanded(
              flex: 3,
              child: m.Column(
                children: [
                  _buildChessboardWithCoordinates(),
                  const m.SizedBox(height: 10),
                  _buildNavButtons(),
                ],
              ),
            ),
            _buildMovePanel(moveRows),
          ],
        ),
      ),
    );
  }

  // ================= UI HELPERS =============================================

  m.Widget _buildChessboardWithCoordinates() {
    const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
    const ranks = ["8", "7", "6", "5", "4", "3", "2", "1"];

    return m.LayoutBuilder(
      builder: (context, constraints) {
        final boardSize = constraints.maxWidth;  
        final squareSize = boardSize / 8;

        return m.Column(
          children: [
            // Files (top)
            m.Row(
              mainAxisAlignment: m.MainAxisAlignment.spaceAround,
              children: files.map((f) => m.Text(
                f,
                style: const m.TextStyle(color: m.Colors.white70),
              )).toList(),
            ),

            // Body: ranks + board + ranks
            m.Row(
              crossAxisAlignment: m.CrossAxisAlignment.center,
              children: [
                // Left ranks – auto-sized
                m.Column(
                  mainAxisAlignment: m.MainAxisAlignment.spaceBetween,
                  children: ranks.map((r) => m.SizedBox(
                    height: squareSize,
                    width: 24,
                    child: m.Center(
                      child: m.Text(
                        r,
                        style: const m.TextStyle(color: m.Colors.white70),
                      ),
                    ),
                  )).toList(),
                ),

                // Board
                m.Expanded(
                  child: ChessBoard(
                    controller: _controller,
                    boardColor: BoardColor.brown,
                    enableUserMoves: true,
                  ),
                ),

                // Right ranks – auto-sized
                m.Column(
                  mainAxisAlignment: m.MainAxisAlignment.spaceBetween,
                  children: ranks.map((r) => m.SizedBox(
                    height: squareSize,
                    width: 24,
                    child: m.Center(
                      child: m.Text(
                        r,
                        style: const m.TextStyle(color: m.Colors.white70),
                      ),
                    ),
                  )).toList(),
                ),
              ],
            ),

            // Files (bottom)
            m.Row(
              mainAxisAlignment: m.MainAxisAlignment.spaceAround,
              children: files.map((f) => m.Text(
                f,
                style: const m.TextStyle(color: m.Colors.white70),
              )).toList(),
            ),
          ],
        );
      },
    );
  }





  m.Widget _buildChatPanel() {
    return m.Expanded(
      flex: 3,
      child: m.Column(
        children: [
          m.Expanded(
            child: m.Container(
              padding: const m.EdgeInsets.all(12),
              decoration: m.BoxDecoration(
                color: panelBackground,
                borderRadius: m.BorderRadius.circular(8),
              ),
              child: m.SingleChildScrollView(
                child: m.Text(
                  chatResponse.isEmpty
                      ? "this is a chat field output for the LLM"
                      : chatResponse,
                  style: const m.TextStyle(fontSize: 16, color: m.Colors.white),
                ),
              ),
            ),
          ),
          const m.SizedBox(height: 10),
          m.TextField(
            controller: chatController,
            style: const m.TextStyle(color: m.Colors.white),
            decoration: m.InputDecoration(
              hintText: "Ask anything or paste PGN...",
              hintStyle: const m.TextStyle(color: m.Colors.white70),
              border: const m.OutlineInputBorder(),
              filled: true,
              fillColor: panelBackground,
            ),
          ),
          const m.SizedBox(height: 10),
          m.Row(
            mainAxisAlignment: m.MainAxisAlignment.spaceEvenly,
            children: [
              m.ElevatedButton(
                onPressed: _sendChat,
                style: m.ElevatedButton.styleFrom(
                    backgroundColor: goldAccent,
                    foregroundColor: m.Colors.black),
                child: const m.Text("Send"),
              ),
              m.ElevatedButton(
                onPressed: _analyzePosition,
                style: m.ElevatedButton.styleFrom(
                    backgroundColor: goldAccent,
                    foregroundColor: m.Colors.black),
                child: const m.Text("Analyze Position"),
              ),
            ],
          ),
        ],
      ),
    );
  }

  m.Widget _buildNavButtons() {
    return m.Row(
      mainAxisAlignment: m.MainAxisAlignment.spaceEvenly,
      children: [
        m.ElevatedButton(
          onPressed: goToStart,
          style: m.ElevatedButton.styleFrom(
              backgroundColor: woodBrown, foregroundColor: m.Colors.white),
          child: const m.Text("⏮ Start"),
        ),
        m.ElevatedButton(
          onPressed: goToPrev,
          style: m.ElevatedButton.styleFrom(
              backgroundColor: woodBrown, foregroundColor: m.Colors.white),
          child: const m.Text("◀ Prev"),
        ),
        m.ElevatedButton(
          onPressed: goToNext,
          style: m.ElevatedButton.styleFrom(
              backgroundColor: woodBrown, foregroundColor: m.Colors.white),
          child: const m.Text("Next ▶"),
        ),
        m.ElevatedButton(
          onPressed: goToEnd,
          style: m.ElevatedButton.styleFrom(
              backgroundColor: woodBrown, foregroundColor: m.Colors.white),
          child: const m.Text("End ⏭"),
        ),
      ],
    );
  }

  m.Widget _buildMovePanel(int moveRows) {
    return m.Expanded(
      flex: 2,
      child: m.Column(
        crossAxisAlignment: m.CrossAxisAlignment.start,
        children: [
          const m.Text("Best Move:",
              style: m.TextStyle(
                  fontSize: 16,
                  fontWeight: m.FontWeight.bold,
                  color: goldAccent)),
          const m.SizedBox(height: 4),
          m.Text(topMoves.trim(),
              style: const m.TextStyle(
                  fontSize: 16,
                  fontWeight: m.FontWeight.bold,
                  color: goldAccent)),
          const m.SizedBox(height: 12),
          const m.Text("Move List:",
              style: m.TextStyle(
                  fontSize: 16,
                  fontWeight: m.FontWeight.bold,
                  color: goldAccent)),
          const m.SizedBox(height: 4),

          m.Expanded(
            child: m.Container(
              padding: const m.EdgeInsets.all(8),
              decoration: m.BoxDecoration(
                  color: panelBackground,
                  borderRadius: m.BorderRadius.circular(8)),
              child: m.Scrollbar(
                thumbVisibility: true,
                child: m.ListView.builder(
                  itemCount: moveRows,
                  itemBuilder: (context, rowIndex) {
                    final moveNumber = rowIndex + 1;
                    final whiteIndex = rowIndex * 2;
                    final blackIndex = whiteIndex + 1;

                    final whiteMove =
                        whiteIndex < moveHistory.length ? moveHistory[whiteIndex] : "";
                    final blackMove =
                        blackIndex < moveHistory.length ? moveHistory[blackIndex] : "";

                    final lastIdx = currentMoveIndex > 0 ? currentMoveIndex - 1 : -1;

                    final whiteHighlighted = whiteIndex == lastIdx;
                    final blackHighlighted = blackIndex == lastIdx;

                    return m.Container(
                      padding: const m.EdgeInsets.symmetric(vertical: 4, horizontal: 6),
                      child: m.Row(
                        children: [
                          m.SizedBox(
                            width: 28,
                            child: m.Text("$moveNumber.",
                                style: const m.TextStyle(
                                    fontSize: 16, color: m.Colors.white70)),
                          ),
                          m.Expanded(
                            child: m.Text(
                              whiteMove,
                              style: m.TextStyle(
                                  fontSize: 16,
                                  color: whiteHighlighted
                                      ? goldAccent
                                      : m.Colors.white),
                            ),
                          ),
                          m.Expanded(
                            child: m.Text(
                              blackMove,
                              style: m.TextStyle(
                                  fontSize: 16,
                                  color: blackHighlighted
                                      ? goldAccent
                                      : m.Colors.white),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ================= BACKEND CALLS =============================================

Future<String> fetchBestMoves(String fen) async {
  final resp = await http.post(
    Uri.parse('$backendUrl/best-move'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'fen': fen}),
  );
  return resp.statusCode == 200
      ? jsonDecode(resp.body)['best_move']
      : 'Error';
}

Future<String> analyzeFen(String fen) async {
  final resp = await http.post(
    Uri.parse('$backendUrl/analyze'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'fen': fen}),
  );
  return resp.statusCode == 200
      ? jsonDecode(resp.body)['analysis']
      : 'Error';
}

Future<String> chatWithLLM(String message, String fen) async {
  final resp = await http.post(
    Uri.parse('$backendUrl/chat'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'message': message, 'fen': fen}),
  );
  return resp.statusCode == 200
      ? jsonDecode(resp.body)['reply']
      : 'Error';
}

Future<Map<String, dynamic>?> loadPGN(String pgn) async {
  final resp = await http.post(
    Uri.parse('$backendUrl/load-pgn'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'pgn': pgn}),
  );
  return resp.statusCode == 200 ? jsonDecode(resp.body) : null;
}
