// Data for the cards
const cardsData = [
    {
        "imageUrl": "Image path",
        "title": "Windows 101",
        "level": "Beginner",
        "price": 2400,
        "description": "Windows 101 provides a comprehensive introduction to the fundamentals of the Windows operating system. From navigating the user interface to managing files and settings, this course equips students with essential skills for using Windows effectively.",
        "classes": 4,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Logic Lab: Breaking the Code",
        "level": "Beginner",
        "price": 8300,
        "description": "In Logic Lab: Breaking the Code, students dive into the world of logic and problem-solving. Through engaging exercises and activities, they learn how to think critically, analyze problems, and develop effective solutions.",
        "classes": 15,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "CodeCraft: C, Java and Python mastery",
        "level": "Advanced",
        "price": 60000,
        "description": "CodeCraft is an advanced course designed to master three popular programming languages: C, Java, and Python. Students learn advanced programming concepts, algorithm design, and software development best practices.",
        "classes": 125,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Web Wizardry: Html, Css and Javascript",
        "level": "Intermediate",
        "price": 18000,
        "description": "Web Wizardry introduces students to the foundations of web development, including HTML, CSS, and JavaScript. Through hands-on projects, they learn how to create dynamic and interactive web pages.",
        "classes": 30,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Game Geniuses",
        "level": "Intermediate",
        "price": 22000,
        "description": "Game Geniuses is a course for aspiring game developers. Students explore game design principles, learn to create game assets, and build their own games using industry-standard tools.",
        "classes": 30,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Intro to OS: Understanding different operating systems",
        "level": "Beginner",
        "price": 1000,
        "description": "Intro to OS provides an overview of various operating systems, including Windows, macOS, and Linux. Students learn about the key features and functionalities of each OS, helping them make informed decisions about their computing needs.",
        "classes": 17,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Basics of CLI",
        "level": "Intermediate",
        "price": 7999,
        "description": "Basics of CLI is a hands-on course that introduces students to the Command-Line Interface (CLI). They learn essential commands and techniques for navigating and managing files and directories in a terminal environment.",
        "classes": 10,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Networking",
        "level": "Intermediate",
        "price": 8999,
        "description": "Networking covers the fundamentals of computer networking, including network architectures, protocols, and technologies. Students gain practical experience in configuring and troubleshooting network devices.",
        "classes": 15,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Cybersecurity",
        "level": "Intermediate",
        "price": 12000,
        "description": "Cybersecurity equips students with essential knowledge and skills to protect their digital assets and privacy. They learn about common cyber threats, security best practices, and defensive strategies.",
        "classes": 15,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "AI",
        "level": "Intermediate",
        "price": 19000,
        "description": "AI introduces students to the fascinating world of Artificial Intelligence. They explore key concepts such as machine learning, neural networks, and natural language processing, and learn to develop AI-powered applications.",
        "classes": 25,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Robotics",
        "level": "Intermediate",
        "price": 16000,
        "description": "Robotics offers a hands-on introduction to robotics and automation. Students learn to build and program robots, explore sensors and actuators, and tackle real-world challenges through project-based learning.",
        "classes": 20,
        "audience": "Solo"
    },
    {
        "imageUrl": "Image path",
        "title": "Personal Development",
        "level": "Beginner",
        "price": 9000,
        "description": "Personal Development empowers students to cultivate essential life skills and confidence. Through interactive activities and reflective exercises, they learn to set goals, communicate effectively, and navigate personal challenges.",
        "classes": 12,
        "audience": "Solo"
    }
    // Add more card data as needed
];

// Global variable to store cart items
let cartItems = [];

// Function to create and append cards
function createCard(cardData, index) {
    const cardContainer = document.getElementById("grid-container");

    // Create card element
    const card = document.createElement("div");
    card.classList.add("product-card");
    card.setAttribute("data-index", index); // Add data-index attribute

    // Set card content
    const cardContent = `
        <figure class="card-banner img-holder">
            <img
                src="${cardData.imageUrl}"
                width="370"
                height="220"
                loading="lazy"
                alt="${cardData.title}"
                class="img-cover"
            />
        </figure>
        <div class="abs-badges">
            <ion-icon name="time-outline" aria-hidden="true"></ion-icon>
            <span class="span">${cardData.duration}</span>
        </div>
        <div class="product-card-content">
            <span class="badge">${cardData.level}</span>
            <h3 class="h3 card-title">${cardData.title}</h3>
            <div class="star">
                <div class="rating-wrapper">
                    ${'<ion-icon name="star"></ion-icon>'.repeat(
        Math.floor(cardData.rating)
    )}
                    ${cardData.rating % 1 !== 0
            ? '<ion-icon name="star-half"></ion-icon>'
            : ""
        }
                </div>
                <p class="star-text">(${cardData.rating}/5 Rating)</p>
            </div>
            <data class="amount" value="${cardData.price
        }">$${cardData.price.toFixed(2)}</data>
            <button class="cart-btn">Add to cart</button>
            <p>${cardData.description}</p>
            <ul class="card-content-meta-list">
                <li class="card-content-meta-item">
                    <ion-icon name="library-outline" aria-hidden="true"></ion-icon>
                    <span class="span">${cardData.classes} Classes</span>
                </li>
                <li class="card-content-meta-item">
                    <ion-icon name="people-outline" aria-hidden="true"></ion-icon>
                    <span class="span">${cardData.audience}</span>
                </li>
            </ul>
        </div>
    `;
    card.innerHTML = cardContent;

    // Append card to container
    cardContainer.appendChild(card);
}

// Function to display cards
function displayCards() {
    cardsData.forEach((cardData, index) => {
        createCard(cardData, index);
    });
}

// Function to handle add to cart button click
function addToCart(index) {
    const selectedItem = cardsData[index];
    cartItems.push(selectedItem);
    updateCart();
    updateCartItemCount();
}

// Function to update the cart UI
function updateCart() {
    const cartContainer = document.getElementById("cart-items");
    cartContainer.innerHTML = ""; // Clear previous cart items

    cartItems.forEach((item, index) => {
        const cartItemElement = document.createElement("span");
        cartItemElement.style.display = "flex";
        cartItemElement.style.justifyContent = "space-between";
        cartItemElement.style.alignItems = "center";
        cartItemElement.style.margin = "5px 0px";

        // Set cart item content
        const cartItemContent = `            
            <p style="width:50%px; font-size: 10px; line-height: 13px;">${item.title}</p>
            <p style=" width:30%;  margin-left:5px; font-size:8px;" >$${item.price.toFixed(2)}</p>
            <button type="button" class="remove-btn" data-index="${index}" style="width:30px; height: 30px; padding:5px; background-color:#FF2400; color:white; border-radius:5px;">X</button>
        `;
        cartItemElement.innerHTML = cartItemContent;

        // Append cart item to container
        cartContainer.appendChild(cartItemElement);
    });
}

// Function to update cart item count
function updateCartItemCount() {
    const cartItemCountElement = document.getElementById('cartItemCount');
    cartItemCountElement.textContent = cartItems.length;
}

// Function to handle remove from cart
function removeFromCart(index) {
    cartItems.splice(index, 1); // Remove item from cartItems array
    updateCart(); // Update cart display
    updateCartItemCount(); // Update cart item count
}

// Call the displayCards function when the page loads
window.onload = displayCards;

// Add event listener for "Add to cart" buttons
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("cart-btn")) {
        const cardIndex = event.target.closest(".product-card").getAttribute("data-index");
        addToCart(cardIndex);
    }
});

// Add event listener for "Remove from cart" buttons
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-btn")) {
        const itemIndex = event.target.getAttribute("data-index");
        removeFromCart(itemIndex);
    }
});
