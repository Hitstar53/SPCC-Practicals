import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class RegexParser extends JFrame {
    private DefaultMutableTreeNode root;

    public RegexParser() {
        initializeUI();
    }

    private void initializeUI() {
        root = new DefaultMutableTreeNode("(a|b)*abb#");

        JTree tree = new JTree(root);
        tree.setPreferredSize(new Dimension(400, 300));

        JScrollPane scrollPane = new JScrollPane(tree);
        getContentPane().add(scrollPane);

        setTitle("Regex Parser");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
    }

    private static class TreeNodeData {
        boolean nullable;
        Set<Integer> firstPos;
        Set<Integer> lastPos;

        TreeNodeData() {
            nullable = false;
            firstPos = new HashSet<>();
            lastPos = new HashSet<>();
        }
    }

    private void buildParseTree() {
        // Build parse tree structure here
        // This is a simplified example, not a complete regex parser

        // For demonstration, adding some nodes
        DefaultMutableTreeNode node1 = new DefaultMutableTreeNode(".");
        DefaultMutableTreeNode node2 = new DefaultMutableTreeNode("*");
        DefaultMutableTreeNode node3 = new DefaultMutableTreeNode("|");
        DefaultMutableTreeNode node4 = new DefaultMutableTreeNode("a");
        DefaultMutableTreeNode node5 = new DefaultMutableTreeNode("b");
        DefaultMutableTreeNode node6 = new DefaultMutableTreeNode("a");
        DefaultMutableTreeNode node7 = new DefaultMutableTreeNode("b");
        DefaultMutableTreeNode node8 = new DefaultMutableTreeNode("#");

        root.add(node1);
        node1.add(node2);
        node2.add(node3);
        node3.add(node4);
        node3.add(node5);
        node1.add(node6);
        node1.add(node7);
        root.add(node8);
    }

    private Map<DefaultMutableTreeNode, TreeNodeData> computeAttributes() {
        // Calculate nullable, firstPos, lastPos attributes here
        // This is a simplified example, not a complete implementation

        Map<DefaultMutableTreeNode, TreeNodeData> attributes = new HashMap<>();

        // Initialize attributes for each node in the parse tree
        // ...

        // Calculate attributes by traversing the parse tree
        // ...

        return attributes;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            RegexParser parser = new RegexParser();
            parser.buildParseTree();
            parser.setVisible(true);

            Map<DefaultMutableTreeNode, TreeNodeData> attributes = parser.computeAttributes();

            // Display attributes in a table or console
            for (Map.Entry<DefaultMutableTreeNode, TreeNodeData> entry : attributes.entrySet()) {
                DefaultMutableTreeNode node = entry.getKey();
                TreeNodeData data = entry.getValue();
                System.out.println("Node: " + node.getUserObject() +
                        ", Nullable: " + data.nullable +
                        ", FirstPos: " + data.firstPos +
                        ", LastPos: " + data.lastPos);
            }
        });
    }
}
