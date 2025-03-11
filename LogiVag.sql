-- Table: Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table: Warehouses
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    location TEXT NOT NULL,
    max_capacity INT NOT NULL
);

-- Table: Users
CREATE TABLE users (
    id_card VARCHAR(20) PRIMARY KEY,  -- Using ID card as PK
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    warehouse_id INT NULL, 
    role_id INT NOT NULL,
    status BOOLEAN DEFAULT TRUE,  -- Active/Inactive
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE SET NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Table: Product Categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Table: Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Table: Product Variants (Handles attributes like color, size, and stock)
CREATE TABLE product_variants (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    attribute_name VARCHAR(255) NOT NULL,  
    attribute_value VARCHAR(255) NOT NULL,
    stock INT DEFAULT 0 CHECK (stock >= 0),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Table: Inventory
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    variant_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    UNIQUE (variant_id, warehouse_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE
);

-- Table: Product Movements between Warehouses
CREATE TABLE movements (
    id SERIAL PRIMARY KEY,
    source_warehouse INT NOT NULL,
    destination_warehouse INT NOT NULL,
    user_id VARCHAR(20) NOT NULL,  
    variant_id INT NOT NULL,  
    quantity INT NOT NULL CHECK (quantity > 0),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Pending', 'Completed', 'Canceled')),  
    reason TEXT,
    token UUID DEFAULT gen_random_uuid(),
    FOREIGN KEY (source_warehouse) REFERENCES warehouses(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_warehouse) REFERENCES warehouses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id_card) ON DELETE CASCADE,
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON DELETE CASCADE
);

-- Table: Logs (Audit Table)
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) NULL,  -- User who performed the action (NULL if automatic)
    affected_table VARCHAR(100) NOT NULL,  -- Table where the event occurred
    operation VARCHAR(20) NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')), -- Operation type
    previous_record JSONB,  -- Stores the previous state (if applicable)
    new_record JSONB,  -- Stores the new state (if applicable)
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of the event
    FOREIGN KEY (user_id) REFERENCES users(id_card) ON DELETE SET NULL
);

-- Trigger Function: General Audit
CREATE OR REPLACE FUNCTION general_audit()
RETURNS TRIGGER AS $$
BEGIN
    -- INSERT case
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO logs (user_id, affected_table, operation, new_record, date)
        VALUES (NEW.user_id, TG_TABLE_NAME, 'INSERT', row_to_json(NEW)::JSONB, NOW());

    -- DELETE case
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO logs (user_id, affected_table, operation, previous_record, date)
        VALUES (OLD.user_id, TG_TABLE_NAME, 'DELETE', row_to_json(OLD)::JSONB, NOW());

    -- UPDATE case
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO logs (user_id, affected_table, operation, previous_record, new_record, date)
        VALUES (OLD.user_id, TG_TABLE_NAME, 'UPDATE', row_to_json(OLD)::JSONB, row_to_json(NEW)::JSONB, NOW());
    END IF;

    RETURN NULL; 
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to each table
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_roles
AFTER INSERT OR UPDATE OR DELETE ON roles
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_warehouses
AFTER INSERT OR UPDATE OR DELETE ON warehouses
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_categories
AFTER INSERT OR UPDATE OR DELETE ON categories
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_products
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_product_variants
AFTER INSERT OR UPDATE OR DELETE ON product_variants
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_inventory
AFTER INSERT OR UPDATE OR DELETE ON inventory
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_movements
AFTER INSERT OR UPDATE OR DELETE ON movements
FOR EACH ROW EXECUTE FUNCTION general_audit();

CREATE TRIGGER audit_logs
AFTER INSERT OR UPDATE OR DELETE ON logs
FOR EACH ROW EXECUTE FUNCTION general_audit();
