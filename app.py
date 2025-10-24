import os
import streamlit as st
import replicate
import base64
from io import BytesIO
from PIL import Image
import random

st.set_page_config(page_title="Medieval Portrait Generator", page_icon="🏰", layout="centered")
st.title("Medieval Portrait Generator 🏰")
st.markdown("*Upload thy likeness and receive a most noble description befitting of medieval court!*")
st.markdown("🔥 **Powered by [Replicate](https://replicate.com)** • 🌊 **Deployed on [DigitalOcean](https://www.digitalocean.com/products/app-platform)** • ⚡ **Built with [Streamlit](https://streamlit.io)**")

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    st.error("Missing REPLICATE_API_TOKEN environment variable. Get one at https://replicate.com/account/api-tokens")
    st.stop()

# Initialize Replicate client
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Example lists for AI generation
EXAMPLE_TITLES = ["Sir", "Lady", "Lord", "Dame", "Duke", "Duchess", "Earl", "Countess", "Baron", "Baroness", "Knight", "Squire", "Maiden", "Master", "Mistress"]
EXAMPLE_LOCATIONS = ["the Cubicle", "the Coffee Shop", "the WiFi Router", "the Netflix Queue", "the Zoom Call", "the Instagram Feed"]
EXAMPLE_SKILLS = ["wielder of spreadsheets", "master of microwaves", "guardian of the remote control", "slayer of email notifications", "ruler of WiFi passwords", "sage of memes"]
EXAMPLE_TRAITS = ["possesses the wisdom of a thousand customer service calls", "bears the noble burden of unread messages", "commands the mystical forces of autocorrect"]

def generate_ai_descriptors():
    """Generate new medieval descriptors using AI"""
    try:
        # Generate new titles
        titles_prompt = f"Generate 8 creative medieval titles similar to these examples: {', '.join(EXAMPLE_TITLES[:5])}. Make them funny and modern-medieval fusion. Return as comma-separated list."
        
        titles_output = replicate.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                "prompt": titles_prompt,
                "max_tokens": 100,
                "temperature": 0.8
            }
        )
        
        # Generate new locations  
        locations_prompt = f"Generate 8 funny modern 'locations' for medieval titles, similar to: {', '.join(EXAMPLE_LOCATIONS[:3])}. Format: 'the [modern place]'. Return as comma-separated list."
        
        locations_output = replicate.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                "prompt": locations_prompt,
                "max_tokens": 100,
                "temperature": 0.8
            }
        )
        
        # Generate new skills
        skills_prompt = f"Generate 8 funny medieval 'skills' for modern life, similar to: {', '.join(EXAMPLE_SKILLS[:3])}. Return as comma-separated list."
        
        skills_output = replicate.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                "prompt": skills_prompt,
                "max_tokens": 100,
                "temperature": 0.8
            }
        )
        
        # Parse outputs
        ai_titles = [t.strip().strip('"') for t in str(titles_output).split(',')]
        ai_locations = [l.strip().strip('"') for l in str(locations_output).split(',')]
        ai_skills = [s.strip().strip('"') for s in str(skills_output).split(',')]
        
        return {
            'titles': ai_titles[:8] if len(ai_titles) >= 8 else EXAMPLE_TITLES,
            'locations': ai_locations[:8] if len(ai_locations) >= 8 else EXAMPLE_LOCATIONS,
            'skills': ai_skills[:8] if len(ai_skills) >= 8 else EXAMPLE_SKILLS,
            'traits': EXAMPLE_TRAITS  # Keep traits as examples for now
        }
        
    except Exception as e:
        st.warning(f"AI descriptor generation failed: {e}. Using default lists.")
        return {
            'titles': EXAMPLE_TITLES,
            'locations': EXAMPLE_LOCATIONS,
            'skills': EXAMPLE_SKILLS,
            'traits': EXAMPLE_TRAITS
        }

# Initialize with AI-generated descriptors
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_descriptors():
    return generate_ai_descriptors()

descriptors = get_descriptors()
TITLES = descriptors['titles']
LOCATIONS = descriptors['locations'] 
SKILLS = descriptors['skills']
PERSONALITY_TRAITS = descriptors['traits']

def generate_medieval_description(has_image=False):
    """Generate a ridiculous medieval description"""
    title = random.choice(TITLES)
    location = random.choice(LOCATIONS)
    skill = random.choice(SKILLS)
    trait = random.choice(PERSONALITY_TRAITS)
    
    description = f"""
🏰 **ROYAL PROCLAMATION** 🏰

Hearken all! Before thee stands **{title} [Your Name] of {location}**, 
noble {skill} and {trait}.

By royal decree, this distinguished personage shall be remembered 
throughout the realm for their legendary ability to {random.choice([
    "find the perfect meme for any occasion",
    "remember where they put their keys (sometimes)",
    "distinguish between similar-looking apps",
    "order food without looking at the menu",
    "pretend to understand cryptocurrency",
    "nod knowingly during technical meetings",
    "keep plants alive for more than a week",
    "fold fitted sheets with minimal cursing"
])}.

*Sealed with the Royal Stamp of Ridiculous Importance* 👑
    """
    
    return description.strip()

def create_medieval_image_transformation(image_bytes, full_description, name):
    """Transform image to look medieval and add text overlay using nano-banana"""
    try:
        # Convert uploaded image to base64 for nano-banana
        image_b64 = base64.b64encode(image_bytes).decode()
        data_uri = f"data:image/jpeg;base64,{image_b64}"
        
        # Create a comprehensive prompt for medieval transformation
        medieval_elements = [
            "Add a golden ornate medieval frame around the portrait",
            "Give the person a royal crown or medieval headdress", 
            "Add a flowing medieval cape or royal robes",
            "Include heraldic symbols and coat of arms in the background",
            "Add medieval castle towers in the distant background",
            "Give the scene a warm, candlelit medieval atmosphere",
            "Add some medieval props like a scepter, sword, or royal orb"
        ]
        
        # Randomly select 3-4 elements for variety
        selected_elements = random.sample(medieval_elements, k=random.randint(3, 4))
        
        # Create a shorter, key part of the description for the image
        title_part = ""
        if "stands" in full_description and "of" in full_description:
            # Extract just the title and name part
            try:
                stands_part = full_description.split("stands")[1].split(",")[0].strip()
                title_part = stands_part.replace("**", "").strip()
            except:
                title_part = f"{name} - Royal Personage"
        else:
            title_part = f"{name} - Royal Personage"
        
        prompt = f"""Transform this portrait into a humorous medieval royal painting style. 
        {' '.join(selected_elements)}
        
        MOST IMPORTANT: Keep the original person's face clearly visible and recognizable.
        Transform the image style to medieval royal portrait but preserve the person's identity.
        
        Add a small elegant medieval scroll banner at the bottom with just the title: '{title_part}'
        
        Focus on visual transformation: medieval styling, royal clothing, majestic background.
        Make it look like a classical royal portrait but with modern humorous touches. 
        Use rich medieval colors: deep reds, royal blues, gold accents.
        Make it both majestic and slightly silly in a fun way.
        
        The person should still be clearly recognizable in medieval royal attire."""
        
        output = replicate.run(
            "google/nano-banana",
            input={
                "prompt": prompt,
                "image_input": [data_uri],
                "aspect_ratio": "match_input_image",
                "output_format": "jpg"
            }
        )
        
        # Return the URL of the generated image
        return output
        
    except Exception as e:
        st.error(f"Medieval image transformation failed: {e}")
        return None

def analyze_image_with_ai(image_bytes):
    """Use AI to analyze the image and generate a more specific description"""
    try:
        # Convert image to base64
        image_b64 = base64.b64encode(image_bytes).decode()
        data_uri = f"data:image/jpeg;base64,{image_b64}"
        
        # Use Replicate's LLaVA or similar vision model
        output = replicate.run(
            "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
            input={
                "image": data_uri,
                "prompt": "Describe this person in 2-3 words focusing on their appearance or setting. Be brief and simple."
            }
        )
        
        # Extract key words from AI response
        ai_description = str(output).lower()
        return ai_description
        
    except Exception as e:
        st.warning(f"AI analysis failed: {e}")
        return None

def create_image_with_text_overlay(image_bytes, full_description):
    """Create an image with complete medieval text overlay using nano-banana"""
    try:
        # Convert uploaded image to base64 for nano-banana
        image_b64 = base64.b64encode(image_bytes).decode()
        data_uri = f"data:image/jpeg;base64,{image_b64}"
        
        # Clean up the description for better text overlay
        clean_description = full_description.replace("🏰", "").replace("**", "").replace("*", "").strip()
        
        # Create a prompt for adding the complete medieval text to the image
        prompt = f"""IMPORTANT: Keep the original image completely unchanged. Only add text overlay.
        
        Add elegant medieval scroll text overlay to this image with the royal proclamation: 
        '{clean_description}'
        
        DO NOT modify the original image - only add text overlays on decorative parchment scrolls.
        Keep the person and background exactly as they are in the original photo.
        Place the text on ornate medieval scroll banners that appear to be placed over the image.
        Use medieval calligraphy and make the text readable and elegant.
        The original image should remain fully visible underneath the text scrolls."""
        
        output = replicate.run(
            "google/nano-banana",
            input={
                "prompt": prompt,
                "image_input": [data_uri],
                "aspect_ratio": "match_input_image",
                "output_format": "jpg"
            }
        )
        
        # Return the URL of the generated image
        return output
        
    except Exception as e:
        st.error(f"Image overlay generation failed: {e}")
        return None

def generate_ai_enhanced_description(ai_description, name):
    """Generate medieval description enhanced by AI analysis"""
    title = random.choice(TITLES)
    
    # Try to extract meaningful words from AI description
    descriptor = "the Mysterious"
    if ai_description:
        if any(word in ai_description for word in ["smile", "smiling", "happy"]):
            descriptor = "the Eternally Cheerful"
        elif any(word in ai_description for word in ["serious", "stern", "focused"]):
            descriptor = "the Contemplative"
        elif any(word in ai_description for word in ["glasses", "spectacles"]):
            descriptor = "the Wise-Eyed Scholar"
        elif any(word in ai_description for word in ["beard", "mustache"]):
            descriptor = "the Magnificently Whiskered"
        elif any(word in ai_description for word in ["hat", "cap"]):
            descriptor = "the Crown-Bearer"
        elif any(word in ai_description for word in ["young", "child"]):
            descriptor = "the Youthful"
        elif any(word in ai_description for word in ["outdoor", "outside", "nature"]):
            descriptor = "the Wild Wanderer"
    
    location = random.choice(LOCATIONS)
    skill = random.choice(SKILLS)
    trait = random.choice(PERSONALITY_TRAITS)
    
    description = f"""
🏰 **ROYAL PROCLAMATION** 🏰

Hearken all! Before thee stands **{title} {name} {descriptor} of {location}**, 
noble {skill} and {trait}.

*As divined by the Royal Court's mystical viewing crystal* 🔮

By royal decree, this distinguished personage shall be remembered 
throughout the realm for their legendary prowess in {random.choice([
    "conquering the weekly grocery quest",
    "navigating the treacherous realm of IKEA",
    "mastering the ancient art of untangling earphones",
    "wielding the power of perfect emoji selection",
    "commanding respect from voice assistants",
    "achieving legendary status in online shopping",
    "maintaining the sacred ritual of coffee consumption",
    "defending the realm against spam calls"
])}.

*Sealed with the Royal Stamp of AI-Enhanced Ridiculousness* 👑✨
    """
    
    return description.strip()

# Main app interface
st.markdown("### 📸 Upload thy portrait, noble steed🐴!")

# Add refresh button for AI-generated descriptors
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("*Using AI-generated medieval descriptors for maximum silliness!*")

# Image upload
uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=["jpg", "jpeg", "png"],
    help="Upload a photo to receive your medieval description!"
)

# Name input
name = st.text_input(
    "What shall we call thee?", 
    placeholder="Enter your name (or leave blank for mystery)",
    help="Your royal name for the proclamation"
)

if name == "":
    name = "The Unnamed One"

# Analysis options
analysis_type = st.radio(
    "Choose thy method of royal analysis:",
    ["🎲 Random Royal Description (Fast)", "🔮 AI-Enhanced Analysis (Uses AI vision)"],
    help="Random is instant and silly. AI-Enhanced analyzes your photo for more personalized silliness!"
)

# Image transformation options
image_option = st.radio(
    "Choose thy royal portrait style:",
    [
        "Text-only proclamation", 
        "🖼️ Add medieval text overlay only",
        "👑 Full medieval royal transformation (Recommended!)"
    ],
    help="Text-only is instant. Overlay adds text to your photo. Full transformation turns you into a medieval royal portrait!"
)

create_overlay = image_option == "🖼️ Add medieval text overlay only"
create_medieval = image_option == "👑 Full medieval royal transformation (Recommended!)"

use_ai = analysis_type.startswith("🔮")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Thy noble visage", width=300)
    
    # Generate description button
    if st.button("🏰 Generate Royal Proclamation!", type="primary"):
        
        # Convert image to bytes for processing
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        if use_ai:
            with st.spinner("The royal court's mystical viewing crystal is analyzing thy likeness..."):
                # Get AI analysis
                ai_description = analyze_image_with_ai(img_byte_arr)
                
                # Generate enhanced description
                description = generate_ai_enhanced_description(ai_description, name)
        else:
            # Generate random description instantly
            description = generate_medieval_description(has_image=True)
            # Replace placeholder name
            description = description.replace("[Your Name]", name)
        
        # Display the royal proclamation
        st.success("🎊 Royal Proclamation Complete!")
        st.markdown(description)
        
        # Generate image transformations if requested
        if create_overlay or create_medieval:
            if create_medieval:
                with st.spinner("🎨 The royal court painters are transforming thy portrait into a majestic medieval masterpiece..."):
                    # Use the complete description for the medieval transformation
                    medieval_image = create_medieval_image_transformation(img_byte_arr, description, name)
                    
                    if medieval_image:
                        st.success("👑 Medieval Royal Portrait Complete!")
                        
                        # Display both images side by side
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📸 Original Portrait:**")
                            st.image(image, caption="Thy modern visage", width=300)
                        
                        with col2:
                            st.markdown("**👑 Medieval Royal Portrait:**")
                            # Display the AI-generated medieval image
                            try:
                                # Handle different possible output formats from nano-banana
                                if hasattr(medieval_image, 'url') and callable(getattr(medieval_image, 'url', None)):
                                    image_url = medieval_image.url()
                                    st.image(image_url, caption="Thy royal medieval transformation", width=300)
                                elif hasattr(medieval_image, 'url'):
                                    # url is a property, not a method
                                    st.image(medieval_image.url, caption="Thy royal medieval transformation", width=300)
                                elif isinstance(medieval_image, list) and len(medieval_image) > 0:
                                    # Handle if output is a list
                                    st.image(medieval_image[0], caption="Thy royal medieval transformation", width=300)
                                elif isinstance(medieval_image, str):
                                    # Direct URL string
                                    st.image(medieval_image, caption="Thy royal medieval transformation", width=300)
                                else:
                                    st.image(str(medieval_image), caption="Thy royal medieval transformation", width=300)
                            except Exception as e:
                                st.error(f"Could not display the medieval image: {e}")
                                st.write(f"Debug - Image object type: {type(medieval_image)}")
                                st.write(f"Debug - Image object: {medieval_image}")
                        
                        # Provide download option
                        try:
                            if hasattr(medieval_image, 'read') and callable(getattr(medieval_image, 'read', None)):
                                img_data = medieval_image.read()
                                st.download_button(
                                    label="👑 Download Medieval Royal Portrait",
                                    data=img_data,
                                    file_name=f"medieval_royal_{name.replace(' ', '_')}.jpg",
                                    mime="image/jpeg"
                                )
                            elif hasattr(medieval_image, 'url'):
                                # Provide link to view/download
                                image_url = medieval_image.url if not callable(getattr(medieval_image, 'url', None)) else medieval_image.url()
                                st.markdown(f"[👑 View/Download Medieval Portrait]({image_url})")
                            elif isinstance(medieval_image, str):
                                st.markdown(f"[👑 View/Download Medieval Portrait]({medieval_image})")
                        except Exception as e:
                            st.warning(f"Download not available: {e}")
                            # At least show the image URL for manual download
                            try:
                                if hasattr(medieval_image, 'url'):
                                    image_url = medieval_image.url if not callable(getattr(medieval_image, 'url', None)) else medieval_image.url()
                                    st.code(f"Image URL: {image_url}")
                                elif isinstance(medieval_image, str):
                                    st.code(f"Image URL: {medieval_image}")
                            except:
                                pass
                            
            elif create_overlay:
                with st.spinner("📜 The royal scribes are inscribing thy proclamation upon thy portrait..."):
                    # Use the complete description for the text overlay
                    overlay_image = create_image_with_text_overlay(img_byte_arr, description)
                    
                    if overlay_image:
                        st.success("📜 Royal Portrait with Proclamation Complete!")
                        
                        # Display both images side by side
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Original Portrait:**")
                            st.image(image, caption="Thy noble visage", width=300)
                        
                        with col2:
                            st.markdown("**Royal Proclamation Portrait:**")
                            # Display the AI-generated image with overlay
                            try:
                                if hasattr(overlay_image, 'url') and callable(getattr(overlay_image, 'url', None)):
                                    st.image(overlay_image.url(), caption="Thy proclaimed portrait", width=300)
                                elif hasattr(overlay_image, 'url'):
                                    st.image(overlay_image.url, caption="Thy proclaimed portrait", width=300)
                                elif isinstance(overlay_image, list) and len(overlay_image) > 0:
                                    st.image(overlay_image[0], caption="Thy proclaimed portrait", width=300)
                                else:
                                    st.image(str(overlay_image), caption="Thy proclaimed portrait", width=300)
                            except Exception as e:
                                st.error(f"Could not display the overlay image: {e}")
                                st.write(f"Debug - Image object type: {type(overlay_image)}")
                                st.write(f"Debug - Image object: {overlay_image}")
                        
                        # Provide download option
                        try:
                            if hasattr(overlay_image, 'read'):
                                img_data = overlay_image.read()
                                st.download_button(
                                    label="📜 Download Royal Portrait",
                                    data=img_data,
                                    file_name=f"royal_portrait_{name.replace(' ', '_')}.jpg",
                                    mime="image/jpeg"
                                )
                        except Exception as e:
                            st.warning(f"Download not available: {e}")
        
        # Add some royal flourish
        st.balloons()
        
else:
    st.info("👆 Upload an image above to receive thy royal medieval description!")
    
# Instructions
st.markdown("---")
st.markdown("""
### 📜 How it works:
1. **Upload thy portrait** - Any selfie, photo, or image will do!
2. **Enter thy name** - Or remain mysterious 
3. **Choose analysis type**:
   - 🎲 **Random**: Instant silly medieval description using AI-generated terms
   - 🔮 **AI-Enhanced**: AI analyzes your photo for personalized medieval nonsense
4. **Choose thy portrait style**:
   - 📜 **Text-only**: Just the hilarious proclamation
   - 🖼️ **Text overlay**: Adds medieval text to your photo
   - 👑 **Full medieval**: Complete royal transformation with crown, robes, castle!
5. **Receive thy royal proclamation & portrait!** 👑

### ✨ Medieval Transformation Features:
- **Royal Accessories**: Crowns, medieval headdresses, royal robes
- **Majestic Backgrounds**: Castle towers, heraldic symbols, coat of arms
- **Medieval Atmosphere**: Candlelit ambiance, rich royal colors
- **Humorous Touch**: Classical portrait style with modern silly elements
- **Random Elements**: Each transformation is unique with different medieval props

*Perfect for profile pics, social media, or becoming internet royalty!*
""")

# Replicate Models showcase
st.markdown("### 🔥 Replicate AI Models Used")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **[🦙 LLaMA 3 70B](https://replicate.com/meta/meta-llama-3-70b-instruct)**
    
    Generates creative medieval descriptors, titles, and skills
    """)

with col2:
    st.markdown("""
    **[👁️ LLaVA 13B](https://replicate.com/yorickvp/llava-13b)**
    
    Computer vision for analyzing your photos
    """)

with col3:
    st.markdown("""
    **[🎨 nano-banana](https://replicate.com/google/nano-banana)**
    
    Advanced image editing for medieval transformations
    """)

st.markdown("*Explore these models and more on [Replicate.com](https://replicate.com) 🚀*")

# Fun facts section
with st.expander("🏰 Medieval Fun Facts & AI Features"):
    st.markdown("""
    **Medieval Fun Facts:**
    - Medieval people actually had a great sense of humor! 
    - Court jesters were highly valued and well-paid
    - Many medieval names literally meant things like "John the Bread-Baker" or "Mary of the Big Hill"
    
    **AI Features Used:**
    - **[LLaMA 3 70B](https://replicate.com/meta/meta-llama-3-70b-instruct)**: Generates creative medieval descriptors and analyzes descriptions
    - **[LLaVA 13B](https://replicate.com/yorickvp/llava-13b)**: Computer vision for analyzing uploaded photos
    - **[nano-banana](https://replicate.com/google/nano-banana)**: Advanced image editing for text overlays and medieval transformations
    - **Smart Caching**: Reduces API calls and improves performance
    
    🔗 **Try these models yourself on [Replicate](https://replicate.com)!**
    
    **🛠️ Tech Stack:**
    - **Frontend**: [Streamlit](https://streamlit.io) - The fastest way to build data apps
    - **AI Platform**: [Replicate](https://replicate.com) - Run machine learning models in the cloud
    - **Hosting**: [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) - Deploy apps with ease
    - **Source Code**: [GitHub](https://github.com/elizabethsiegle/medieval-image-proclamation-gen-replicate-dumbthings-demo) - Open source and collaborative
    
    *Your medieval persona is scientifically* calculated using cutting-edge AI (*still not actually scientific)*
    """)

# Sticky footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0e1117;
    color: white;
    text-align: center;
    padding: 10px;
    border-top: 1px solid #262730;
    font-size: 14px;
}
</style>
<div class="footer">
    ⚔️ forged with medieval magic & modern AI 🏰 | <a href="https://replicate.com" style="color: #ff6b6b;">Replicate</a> × <a href="https://www.digitalocean.com/products/app-platform" style="color: #0080ff;">DigitalOcean</a> × <a href="https://streamlit.io" style="color: #ff4b4b;">Streamlit</a> | <a href="https://github.com/elizabethsiegle/medieval-image-proclamation-gen-replicate-dumbthings-demo" style="color: #ffd700;">GitHub</a>
</div>
""", unsafe_allow_html=True)
