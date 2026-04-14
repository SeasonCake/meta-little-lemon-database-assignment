-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema little_lemon
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema little_lemon
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `little_lemon` DEFAULT CHARACTER SET utf8 ;
USE `little_lemon` ;

-- -----------------------------------------------------
-- Table `little_lemon`.`Customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`Customers` (
  `CustomerID` VARCHAR(20) NOT NULL,
  `FullName` VARCHAR(100) NOT NULL,
  `City` VARCHAR(50) NOT NULL,
  `Country` VARCHAR(50) NOT NULL,
  `PostalCode` VARCHAR(20) NOT NULL,
  `CountryCode` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`CustomerID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `little_lemon`.`Staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`Staff` (
  `StaffID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100) NOT NULL,
  `Role` VARCHAR(50) NOT NULL,
  `Salary` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`StaffID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `little_lemon`.`Bookings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`Bookings` (
  `BookingID` INT NOT NULL AUTO_INCREMENT,
  `BookingDate` DATE NOT NULL,
  `TableNumber` INT NOT NULL,
  `CustomerID` VARCHAR(20) NOT NULL,
  `StaffID` INT NOT NULL,
  PRIMARY KEY (`BookingID`),
  INDEX `bookings_customers_idx` (`CustomerID` ASC) VISIBLE,
  INDEX `fk_bookings_staff_idx` (`StaffID` ASC) VISIBLE,
  CONSTRAINT `fk_bookings_customers`
    FOREIGN KEY (`CustomerID`)
    REFERENCES `little_lemon`.`Customers` (`CustomerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bookings_staff`
    FOREIGN KEY (`StaffID`)
    REFERENCES `little_lemon`.`Staff` (`StaffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `little_lemon`.`Menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`Menu` (
  `MenuID` INT NOT NULL AUTO_INCREMENT,
  `CourseName` VARCHAR(100) NOT NULL,
  `CuisineName` VARCHAR(50) NOT NULL,
  `StarterName` VARCHAR(100) NOT NULL,
  `DessertName` VARCHAR(100) NOT NULL,
  `Drink` VARCHAR(100) NOT NULL,
  `Sides` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`MenuID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `little_lemon`.`Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`Orders` (
  `RowNumber` INT NOT NULL,
  `OrderID` VARCHAR(20) NOT NULL,
  `OrderDate` DATE NOT NULL,
  `CustomerID` VARCHAR(20) NOT NULL,
  `MenuID` INT NOT NULL,
  `Quantity` INT NOT NULL,
  `Cost` DECIMAL(10,2) NOT NULL,
  `Sales` DECIMAL(10,2) NOT NULL,
  `Discount` DECIMAL(5,2) NOT NULL,
  INDEX `fk_orders_customers_idx` (`CustomerID` ASC) VISIBLE,
  INDEX `fk_orders_menu_idx` (`MenuID` ASC) VISIBLE,
  PRIMARY KEY (`RowNumber`),
  CONSTRAINT `fk_orders_customers`
    FOREIGN KEY (`CustomerID`)
    REFERENCES `little_lemon`.`Customers` (`CustomerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_menu`
    FOREIGN KEY (`MenuID`)
    REFERENCES `little_lemon`.`Menu` (`MenuID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `little_lemon`.`OrderDeliveryStatus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `little_lemon`.`OrderDeliveryStatus` (
  `DeliveryID` INT NOT NULL AUTO_INCREMENT,
  `RowNumber` INT NOT NULL,
  `DeliveryDate` DATE NOT NULL,
  `DeliveryCost` DECIMAL(10,2) NOT NULL,
  `DeliveryStatus` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`DeliveryID`),
  INDEX `fk_ods_orders_idx` (`RowNumber` ASC) VISIBLE,
  CONSTRAINT `fk_ods_orders`
    FOREIGN KEY (`RowNumber`)
    REFERENCES `little_lemon`.`Orders` (`RowNumber`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
