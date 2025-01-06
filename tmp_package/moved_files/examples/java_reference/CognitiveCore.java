package cognitive.core;

import java.util.*;
import java.time.Instant;

/**
 * Core tag element that supports visitor pattern and metadata tracking.
 */
class TagElement {
    private final String name;
    private final Map<String, String> attributes;
    private final List<TagElement> children;
    private final TagMetadata metadata;

    public TagElement(String name) {
        this.name = name;
        this.attributes = new HashMap<>();
        this.children = new ArrayList<>();
        this.metadata = new TagMetadata();
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
        children.forEach(child -> child.accept(visitor));
    }
}

/**
 * Metadata for tracking tag state and history.
 */
class TagMetadata {
    private final Instant creationTime;
    private final List<String> modificationHistory;
    private int permissionLevel;

    public TagMetadata() {
        this.creationTime = Instant.now();
        this.modificationHistory = new ArrayList<>();
        this.permissionLevel = 0;
    }
}

/**
 * Base visitor interface with type-safe visit methods.
 */
interface Visitor {
    void visit(TagElement element);
    default void beforeVisit(TagElement element) {}
    default void afterVisit(TagElement element) {}
}

/**
 * Context for processing operations with thread-safe state management.
 */
class ProcessingContext {
    private final StringBuilder feedback;
    private final List<String> errors;
    private final Map<String, Object> state;

    public ProcessingContext() {
        this.feedback = new StringBuilder();
        this.errors = Collections.synchronizedList(new ArrayList<>());
        this.state = Collections.synchronizedMap(new HashMap<>());
    }

    public synchronized void addFeedback(String message) {
        feedback.append(message).append("\n");
    }

    public void addError(String error) {
        errors.add(error);
    }
}

/**
 * Main bridge implementation with proper lifecycle management.
 */
public class CognitiveBridge implements AutoCloseable {
    private final ProcessingContext context;
    private final List<Visitor> visitors;
    private final Object lock = new Object();

    public CognitiveBridge() {
        this.context = new ProcessingContext();
        this.visitors = new ArrayList<>();
    }

    public void processInput(String input) {
        TagElement element = new TagElement("user_input");
        element.getAttributes().put("content", input);

        synchronized(lock) {
            visitors.forEach(visitor -> {
                try {
                    visitor.beforeVisit(element);
                    visitor.visit(element);
                    visitor.afterVisit(element);
                } catch (Exception e) {
                    context.addError("Error in visitor: " + e.getMessage());
                }
            });
        }
    }

    @Override
    public void close() {
        // Cleanup resources
        visitors.clear();
    }
}
