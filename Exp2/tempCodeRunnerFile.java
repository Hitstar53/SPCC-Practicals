import java.util.*;

class Node {
    char data;
    Node left, right;

    public Node(char data) {
        this.data = data;
        this.left = this.right = null;
    }
}

public class RegexParser {

    private static int position = 1;

    public static void main(String[] args) {
        String regex = "(a|b)*abb#";
        Node root = buildParseTree(regex);
        printParseTree(root, 0);
        printTable(root);
    }

    private static Node buildParseTree(String regex) {
        Stack<Node> stack = new Stack<>();

        for (char c : regex.toCharArray()) {
            if (c == '(' || c == '|' || c == '*') {
                stack.push(new Node(c));
            } else if (Character.isLetter(c) || c == '#') {
                stack.push(new Node(c));
            } else if (c == ')') {
                Node top = stack.pop();
                Node operand = stack.pop();
                Node operator = stack.pop();

                operator.left = operand;
                operator.right = top;
                stack.push(operator);
            }
        }

        return stack.pop();
    }

    private static void printParseTree(Node root, int level) {
        if (root != null) {
            printParseTree(root.right, level + 1);
            for (int i = 0; i < level; i++) {
                System.out.print("  ");
            }
            System.out.println(root.data);
            printParseTree(root.left, level + 1);
        }
    }

    private static boolean isNullable(Node node) {
        return node.data == '*' || node.data == '#';
    }

    private static Set<Integer> firstPos(Node node) {
        Set<Integer> result = new HashSet<>();
        if (Character.isLetter(node.data)) {
            result.add(position);
        } else if (node.data == '*') {
            result.addAll(firstPos(node.left));
        } else if (node.data == '|') {
            result.addAll(firstPos(node.left));
            result.addAll(firstPos(node.right));
        }
        return result;
    }

    private static Set<Integer> lastPos(Node node) {
        Set<Integer> result = new HashSet<>();
        if (Character.isLetter(node.data)) {
            result.add(position);
        } else if (node.data == '*') {
            result.addAll(lastPos(node.left));
        } else if (node.data == '|') {
            result.addAll(lastPos(node.left));
            result.addAll(lastPos(node.right));
        }
        return result;
    }

    private static Set<Integer> followPos(Node node) {
        Set<Integer> result = new HashSet<>();
        if (node.data == '|') {
            result.addAll(followPos(node.left));
            result.addAll(followPos(node.right));
        } else if (node.data == '*') {
            Set<Integer> lastPosLeft = lastPos(node.left);
            Set<Integer> firstPosLeft = firstPos(node.left);
            for (int pos : lastPosLeft) {
                result.addAll(firstPosLeft);
            }
        }
        return result;
    }

    private static void printTable(Node root) {
        System.out.println("Node\tNullable\tFirstPos\tFollowPos\tLastPos");
        System.out.println("---------------------------------------------");
        printTableRow(root);
    }

    private static void printTableRow(Node node) {
        System.out.print(node.data + "\t" + isNullable(node) + "\t\t");
        Set<Integer> firstPosSet = firstPos(node);
        printSet(firstPosSet);
        System.out.print("\t\t");
        Set<Integer> followPosSet = followPos(node);
        printSet(followPosSet);
        System.out.print("\t\t");
        Set<Integer> lastPosSet = lastPos(node);
        printSet(lastPosSet);
        System.out.println();

        if (node.left != null) {
            printTableRow(node.left);
        }

        if (node.right != null) {
            printTableRow(node.right);
        }
    }

    private static void printSet(Set<Integer> set) {
        System.out.print("{");
        for (int pos : set) {
            System.out.print(pos + ",");
        }
        System.out.print("}");
    }
}
