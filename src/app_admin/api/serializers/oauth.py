from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token

from app_user.models import UserModel
from app_admin.models import AdminModel

from utils.base_errors import BaseErrors

import requests
import json

data = {
    "Bachelor": {
        "items": [
            {
                "label": "دانشکده معماري و شهرسازي",
                "value": "School of Architecture and Environmental Design",
            },
            {
                "label": "دانشکده مهندسي شيمي، نفت و گاز",
                "value": "School of Chemical Petroleum and Gas Engineering",
            },
            {
                "label": "دانشکده مهندسي عمران",
                "value": "School of Civil Engineering",
            },
            {
                "label": "دانشکده مهندسی کامپیوتر",
                "value": "School of Computer Engineering",
            },
            {
                "label": "دانشکده مهندسي برق",
                "value": "School of Electrical Engineering",
            },
            {
                "label": "دانشکده مهندسي صنايع",
                "value": "School of Industrial Engineering",
            },
            {
                "label": "دانشکده  رياضي",
                "value": "School of Mathematics",
            },
            {
                "label": "دانشکده مهندسي مکانيک",
                "value": "School of Mechanical Engineering",
            },
            {
                "label": "دانشکده مواد و متالورژي",
                "value": "School of Metallurgy and Materials Engineering",
            },
            {
                "label": "دانشکده  فيزيک",
                "value": "School of Physics",
            },
            {
                "label": "دانشکده مهندسي راه آهن",
                "value": "School of Railway Engineering",
            },
        ],
        "data": {
            "School of Architecture and Environmental Design": [
                {
                    "label": "معماری",
                    "value": "Architecture",
                },
                {
                    "label": "طراحی صنعتی",
                    "value": "Industrial Design",
                },
            ],
            "School of Chemical Petroleum and Gas Engineering": [
                {
                    "label": "مهندسی شیمی",
                    "value": "Chemical Engineering",
                },
            ],
            "School of Civil Engineering": [
                {
                    "label": "مهندسی عمران",
                    "value": "Civil Engineering",
                },
            ],
            "School of Computer Engineering": [
                {
                    "label": "مهندسی سخت افزار",
                    "value": "Hardware Engineering",
                },
                {
                    "label": "مهندسی نرم افزار",
                    "value": "Software Engineering",
                },
            ],
            "School of Electrical Engineering": [
                {
                    "label": "سیستم های ارتباطی",
                    "value": "Communication Systems",
                },
                {
                    "label": "سیستم های قدرت",
                    "value": "Power Systems",
                },
                {
                    "label": "الکترونیک",
                    "value": "Electronics",
                },
                {
                    "label": "سیستمهای کنترل",
                    "value": "Control Systems",
                },
            ],
            "School of Industrial Engineering": [
                {
                    "label": "مهندسی صنایع",
                    "value": "Industrial Engineering",
                },
            ],
            "School of Mathematics": [
                {
                    "label": "ریاضیات و کاربردهای آن",
                    "value": "Mathematics and Its Applications",
                },
            ],
            "School of Mechanical Engineering": [
                {
                    "label": "مهندسی مکانیک",
                    "value": "Mechanical Engineering",
                },
            ],
            "School of Metallurgy and Materials Engineering": [
                {
                    "label": "مهندسی مواد و متالورژی",
                    "value": "Material and Metallurgical Engineering",
                },
            ],
            "School of Physics": [
                {
                    "label": "فیزیک اتمی و مولکولی",
                    "value": "Atomic and Molecular Physics",
                },
                {
                    "label": "فیزیک حالت جامد",
                    "value": "Solid State Physics",
                },
            ],
            "School of Railway Engineering": [
                {
                    "label": "مهندسی حمل و نقل ریلی",
                    "value": "Railway Transportation Engineering",
                },
                {
                    "label": "مهندسی سهام نورد راه آهن",
                    "value": "Railway Rolling Stock Engineering",
                },
                {
                    "label": "مهندسی راه آهن و سازه",
                    "value": "Railway Track and Structures Engineering",
                },
            ],
        },
    },
    "Master": {
        "items": [
            {
                "label": "دانشکده  شيمي",
                "value": "Department of Chemistry",
            },
            {
                "label": "دانشکده علوم پايه",
                "value": "Department of Foreign Language",
            },
            {
                "label": "دانشکده معماري و شهرسازي",
                "value": "School of Architecture and Environmental Design",
            },
            {
                "label": "دانشکده مهندسي خودرو",
                "value": "School of Automotive Engineering",
            },
            {
                "label": "دانشکده مهندسي شيمي، نفت و گاز",
                "value": "School of Chemical Petroleum and Gas Engineering",
            },
            {
                "label": "دانشکده مهندسي عمران",
                "value": "School of Civil Engineering",
            },
            {
                "label": "دانشکده مهندسی کامپیوتر",
                "value": "School of Computer Engineering",
            },
            {
                "label": "دانشکده مهندسي برق",
                "value": "School of Electrical Engineering",
            },
            {
                "label": "دانشکده مهندسي صنايع",
                "value": "School of Industrial Engineering",
            },
            {
                "label": "دانشکده  رياضي",
                "value": "School of Mathematics",
            },
            {
                "label": "دانشکده مهندسي مکانيک",
                "value": "School of Mechanical Engineering",
            },
            {
                "label": "دانشکده مواد و متالورژي",
                "value": "School of Metallurgy and Materials Engineering",
            },
            {
                "label": "دانشکده فناوريهای نوين",
                "value": "School of Advanced Technologies",
            },
            {
                "label": "دانشکده  فيزيک",
                "value": "School of Physics",
            },
            {
                "label": "دانشکده مهندسي پيشرفت",
                "value": "School of Management Economy and Progress Engineering",
            },
            {
                "label": "دانشکده مهندسي راه آهن",
                "value": "School of Railway Engineering",
            },
        ],
        "data": {
            "Department of Chemistry": [
                {
                    "label": "شیمی تجزیه",
                    "value": "Analytical Chemistry",
                },
                {
                    "label": "شیمی معدنی",
                    "value": "Inorganic Chemistry",
                },
                {
                    "label": "شیمی ارگانیک",
                    "value": "Organic Chemistry",
                },
                {
                    "label": "شیمی فیزیک",
                    "value": "Physical Chemistry",
                },
                {
                    "label": "نانو شیمی",
                    "value": "Nano-Chemistry",
                },
            ],
            "Department of Foreign Language": [
                {
                    "label": "تدریس زبان انگلیسی به عنوان یک زبان خارجی",
                    "value": "Teaching English as a Foreign Language",
                },
            ],
            "School of Architecture and Environmental Design": [
                {
                    "label": "برنامه ریزی منطقه ای",
                    "value": "Regional Planning",
                },
                {
                    "label": "معماری",
                    "value": "Architecture",
                },
                {
                    "label": "معماری - مسکن",
                    "value": "Architecture - Housing",
                },
                {
                    "label": "معماری - پایدار",
                    "value": "Architecture - Sustainable",
                },
                {
                    "label": "معماری - فناوری",
                    "value": "Architecture - Technology",
                },
                {
                    "label": "معماری - فضاهای فرهنگی و آموزشی",
                    "value": "Architecture - Cultural and Educational Spaces",
                },
                {
                    "label": "معماری - فضاهای مراقبت بهداشتی",
                    "value": "Architecture - Health Care Spaces",
                },
                {
                    "label": "معماری فضاهای زمین",
                    "value": "Land Spaces Architecture",
                },
                {
                    "label": "طراحی صنعتی",
                    "value": "Industrial Design",
                },
                {
                    "label": "حفاظت و مرمت ابنیه و پارچه های تاریخی - حفاظت و احیای میراث شهری",
                    "value": "Conservation and Restoration of Historical Buildings and Fabrics – Conservation and Restoration of Urban Heritage",
                },
                {
                    "label": "حفاظت و مرمت ابنیه و پارچه های تاریخی - حفاظت و مرمت میراث معماری",
                    "value": "Conservation and Restoration of Historical Buildings and Fabrics – Conservation and Restoration of Architectural Heritage",
                },
                {
                    "label": "طراحی شهری",
                    "value": "Urban Design",
                },
                {
                    "label": "برنامه ریزی شهری",
                    "value": "Urban Planning",
                },
            ],
            "School of Automotive Engineering": [
                {
                    "label": "مهندسی خودرو - طراحی سیستم های دینامیک خودرو",
                    "value": "Automotive Engineering - Automobile Dynamic Systems Design",
                },
                {
                    "label": "مهندسی خودرو - قطار برق",
                    "value": "Automotive Engineering - Power Train",
                },
                {
                    "label": "مهندسی خودرو - بدنه و سازه",
                    "value": "Automotive Engineering - Body and Structure",
                },
                {
                    "label": "مهندسی خودرو - الکترونیک خودرو و مهندسی برق",
                    "value": "Automotive Engineering - Automotive Electronics & Electrical Engineering",
                },
            ],
            "School of Chemical Petroleum and Gas Engineering": [
                {
                    "label": "شبیه سازی و کنترل مدل سازی فرآیند",
                    "value": "Process Modeling Simulation & Control",
                },
                {
                    "label": "مهندسی شیمی معدنی",
                    "value": "Mineral Chemical Engineering",
                },
                {
                    "label": "فرایندهای جداسازی",
                    "value": "Separation Processes",
                },
                {
                    "label": "سینتیک و کاتالیز",
                    "value": "Kinetic and Catalysis",
                },
                {
                    "label": "ترمودینامیک",
                    "value": "Thermodynamics",
                },
                {
                    "label": "مهندسی پلیمر",
                    "value": "Polymer Engineering",
                },
                {
                    "label": "مهندسی مخازن هیدروکربن",
                    "value": "Hydrocarbon Reservoir Engineering",
                },
                {
                    "label": "مهندسی طراحی فرآیند",
                    "value": "Process Design Engineering",
                },
            ],
            "School of Civil Engineering": [
                {
                    "label": "مهندسی سازه",
                    "value": "Structural Engineering",
                },
                {
                    "label": "مهندسی زلزله",
                    "value": "Earthquake Engineering",
                },
                {
                    "label": "مدیریت و مهندسی ساخت و ساز",
                    "value": "Construction Management and Engineering",
                },
                {
                    "label": "مهندسی ژئوتکنیک",
                    "value": "Geotechnical Engineering",
                },
                {
                    "label": "مهندسی راه و ترابری",
                    "value": "Road and Transportation Engineering",
                },
                {
                    "label": "حمل و نقل",
                    "value": "Transportation",
                },
                {
                    "label": "مدیریت منابع آب",
                    "value": "Water Resources Management",
                },
                {
                    "label": "مهندسی آب و سازه های هیدرولیک",
                    "value": "Water Engineering and Hydraulic Structures",
                },
                {
                    "label": "مهندسی محیط زیست",
                    "value": "Environmental Engineering",
                },
                {
                    "label": "مهندسی سازه های دریایی",
                    "value": "Marine Structures Engineering",
                },
            ],
            "School of Computer Engineering": [
                {
                    "label": "مهندسی نرم افزار",
                    "value": "Software Engineering",
                },
                {
                    "label": "هوش مصنوعی و رباتیک",
                    "value": "Artificial Intelligence & Robotics",
                },
                {
                    "label": "معماری سیستم های کامپیوتری",
                    "value": "Computer Systems Architecture",
                },
                {
                    "label": "مهندسی کامپیوتر - شبکه های کامپیوتری",
                    "value": "Computer Engineering - Computer Networks",
                },
            ],
            "School of Electrical Engineering": [
                {
                    "label": "سیستم های ارتباطی",
                    "value": "Communication Systems",
                },
                {
                    "label": "سیستم های قدرت",
                    "value": "Power Systems",
                },
                {
                    "label": "سیستمهای کنترل",
                    "value": "Control Systems",
                },
                {
                    "label": "بیو الکتریک",
                    "value": "Bio-Electrics",
                },
                {
                    "label": "سیستم های الکترونیک دیجیتال",
                    "value": "Digital Electronic Systems",
                },
                {
                    "label": "مدارهای مجتمع الکترونیکی",
                    "value": "Electronic Integrated Circuits",
                },
                {
                    "label": "ماشین های الکتریکی و الکترونیک قدرت",
                    "value": "Electrical Machines and Power Electronics",
                },
                {
                    "label": "میدان ها و امواج الکترومغناطیسی",
                    "value": "Electromagnetic Fields and Waves",
                },
            ],
            "School of Industrial Engineering": [
                {
                    "label": "مهندسی فناوری اطلاعات - تجارت الکترونیک",
                    "value": "Information Technology Engineering - Electronic Commerce",
                },
                {
                    "label": "بهینه سازی سیستم",
                    "value": "Systems Optimization",
                },
                {
                    "label": "زنجیره تامین و مهندسی لجستیک",
                    "value": "Supply Chain and Logistic Engineering",
                },
                {
                    "label": "مدیریت مهندسی",
                    "value": "Engineering Management",
                },
                {
                    "label": "سیستم های کلان اجتماعی-اقتصادی",
                    "value": "Socio-Economic Macro Systems",
                },
                {
                    "label": "مدیریت پروژه",
                    "value": "Project Management",
                },
                {
                    "label": "مهندسی مالی",
                    "value": "Financial Engineering",
                },
            ],
            "School of Mathematics": [
                {
                    "label": "ریاضیات محض - جبر",
                    "value": "Pure Mathematics - Algebra",
                },
                {
                    "label": "ریاضی محض - هندسه",
                    "value": "Pure Mathematics - Geometry",
                },
                {
                    "label": "ریاضیات محض - تجزیه و تحلیل",
                    "value": "Pure Mathematics - Analysis",
                },
                {
                    "label": "ریاضی کاربردی - تحلیل عددی",
                    "value": "Applied Mathematics - Numerical Analysis",
                },
                {
                    "label": "ریاضیات کاربردی - تحقیق در عملیات",
                    "value": "Applied Mathematics - Operation Research",
                },
                {
                    "label": "آمار ریاضیات",
                    "value": "Mathematics Statistics",
                },
            ],
            "School of Mechanical Engineering": [
                {
                    "label": "طراحی کاربردی",
                    "value": "Applied Design",
                },
                {
                    "label": "تبدیل انرژی",
                    "value": "Energy Conversion",
                },
                {
                    "label": "تولید",
                    "value": "Manufacturing",
                },
                {
                    "label": "بیومکانیک",
                    "value": "Biomechanics",
                },
            ],
            "School of Metallurgy and Materials Engineering": [
                {
                    "label": "متالورژی استخراجی",
                    "value": "Extractive Metallurgy",
                },
                {
                    "label": "مهندسی سرامیک",
                    "value": "Ceramics Engineering",
                },
                {
                    "label": "انتخاب مواد",
                    "value": "Materials Selection",
                },
                {
                    "label": "مواد زیستی",
                    "value": "Bio-Materials",
                },
                {
                    "label": "ریخته گری فلزات",
                    "value": "Metals Casting",
                },
                {
                    "label": "شکل گیری فلزات",
                    "value": "Metals Forming",
                },
            ],
            "School of Advanced Technologies": [
                {
                    "label": "نانو فناوری - مواد",
                    "value": "Nanotechnology - Materials",
                },
                {
                    "label": "سیستم های انرژی - انرژی و محیط زیست",
                    "value": "Energy Systems - Energy and Environment",
                },
                {
                    "label": "مهندسی ماهواره",
                    "value": "Satellite Engineering",
                },
            ],
            "School of Physics": [
                {
                    "label": "فتونیک",
                    "value": "Photonics",
                },
                {
                    "label": "فیزیک ماده متراکم",
                    "value": "Condensed Matter Physics",
                },
                {
                    "label": "فیزیک اپتیک لیزر",
                    "value": "Laser Optics Physics",
                },
            ],
            "School of Management Economy and Progress Engineering": [
                {
                    "label": "کارشناس ارشد مدیریت بازرگانی (MBA) - بازاریابی",
                    "value": "Master of Business Administration (MBA) - Marketing",
                },
                {
                    "label": "کارشناس ارشد مدیریت بازرگانی (MBA) - استراتژی",
                    "value": "Master of Business Administration (MBA) - Strategy",
                },
                {
                    "label": "مدیریت فناوری (MOT) - نوآوری فناوری",
                    "value": "Management of Technology (MOT) - Technological Innovation",
                },
                {
                    "label": "مدیریت فناوری (MOT) - انتقال فناوری",
                    "value": "Management of Technology (MOT) - Technological Transfer",
                },
                {
                    "label": "مدیریت فناوری (MOT) - سیاست های تحقیق و توسعه",
                    "value": "Management of Technology (MOT) - Research & Development Policies",
                },
                {
                    "label": "مدیریت فناوری اطلاعات - کسب و کار الکترونیکی",
                    "value": "Information Technology Management-E-Business",
                },
                {
                    "label": "کارآفرینی - کسب و کارهای جدید",
                    "value": "Entrepreneurship - New Businesses",
                },
                {
                    "label": "مهندسی صنایع - سیستم های کلان",
                    "value": "Industrial Engineering - Macro Systems",
                },
                {
                    "label": "توسعه اقتصادی و برنامه ریزی",
                    "value": "Economic Development and Planning",
                },
                {
                    "label": "برنامه ریزی سیستم های اقتصادی",
                    "value": "Economic Systems Planning",
                },
            ],
            "School of Railway Engineering": [
                {
                    "label": "مهندسی حمل و نقل ریلی",
                    "value": "Railway Transportation Engineering",
                },
                {
                    "label": "مهندسی سهام نورد راه آهن",
                    "value": "Railway Rolling Stock Engineering",
                },
                {
                    "label": "مهندسی راه آهن و سازه",
                    "value": "Railway Track and Structures Engineering",
                },
                {
                    "label": "مهندسی راه آهن برق",
                    "value": "Electric Railways Engineering",
                },
                {
                    "label": "مهندسی ایمنی راه آهن",
                    "value": "Railway Safety Engineering",
                },
                {
                    "label": "کنترل و سیگنالینگ راه آهن",
                    "value": "Railway Control and Signaling",
                },
            ],
        },
    },
    "P.H.D": {
        "items": [
            {
                "label": "دانشکده  شيمي",
                "value": "Department of Chemistry",
            },
            {
                "label": "دانشکده معماري و شهرسازي",
                "value": "School of Architecture and Environmental Design",
            },
            {
                "label": "دانشکده مهندسي خودرو",
                "value": "School of Automotive Engineering",
            },
            {
                "label": "دانشکده مهندسي شيمي، نفت و گاز",
                "value": "School of Chemical Petroleum and Gas Engineering",
            },
            {
                "label": "دانشکده مهندسي عمران",
                "value": "School of Civil Engineering",
            },
            {
                "label": "دانشکده مهندسی کامپیوتر",
                "value": "School of Computer Engineering",
            },
            {
                "label": "دانشکده مهندسي برق",
                "value": "School of Electrical Engineering",
            },
            {
                "label": "دانشکده مهندسي صنايع",
                "value": "School of Industrial Engineering",
            },
            {
                "label": "دانشکده  رياضي",
                "value": "School of Mathematics",
            },
            {
                "label": "دانشکده مهندسي مکانيک",
                "value": "School of Mechanical Engineering",
            },
            {
                "label": "دانشکده مواد و متالورژي",
                "value": "School of Metallurgy and Materials Engineering",
            },
            {
                "label": "دانشکده  فيزيک",
                "value": "School of Physics",
            },
            {
                "label": "دانشکده مهندسي پيشرفت",
                "value": "School of Management Economy and Progress Engineering",
            },
            {
                "label": "دانشکده مهندسي راه آهن",
                "value": "School of Railway Engineering",
            },
        ],
        "data": {
            "Department of Chemistry": [
                {
                    "label": "شیمی تجزیه",
                    "value": "Analytical Chemistry",
                },
                {
                    "label": "شیمی معدنی",
                    "value": "Inorganic Chemistry",
                },
                {
                    "label": "شیمی ارگانیک",
                    "value": "Organic Chemistry",
                },
                {
                    "label": "شیمی فیزیک",
                    "value": "Physical Chemistry",
                },
            ],
            "School of Architecture and Environmental Design": [
                {
                    "label": "معماری",
                    "value": "Architecture",
                },
                {
                    "label": "شهرسازی",
                    "value": "Urbanism",
                },
            ],
            "School of Automotive Engineering": [
                {
                    "label": "مهندسی خودرو - طراحی سیستم های دینامیک خودرو",
                    "value": "Automotive Engineering - Automobile Dynamic Systems Design",
                },
                {
                    "label": "مهندسی خودرو - قطار برق",
                    "value": "Automotive Engineering - Power Train",
                },
                {
                    "label": "مهندسی خودرو - بدنه و سازه",
                    "value": "Automotive Engineering - Body and Structure",
                },
            ],
            "School of Chemical Petroleum and Gas Engineering": [
                {
                    "label": "مهندسی شیمی",
                    "value": "Chemical Engineering",
                },
            ],
            "School of Civil Engineering": [
                {
                    "label": "مهندسی سازه",
                    "value": "Structural Engineering",
                },
                {
                    "label": "مهندسی زلزله",
                    "value": "Earthquake Engineering",
                },
                {
                    "label": "مدیریت و مهندسی ساخت و ساز",
                    "value": "Construction Management and Engineering",
                },
                {
                    "label": "مهندسی ژئوتکنیک",
                    "value": "Geotechnical Engineering",
                },
                {
                    "label": "مهندسی راه و ترابری",
                    "value": "Road and Transportation Engineering",
                },
                {
                    "label": "حمل و نقل",
                    "value": "Transportation",
                },
                {
                    "label": "مدیریت منابع آب",
                    "value": "Water Resources Management",
                },
                {
                    "label": "مهندسی آب و سازه های هیدرولیک",
                    "value": "Water Engineering and Hydraulic Structures",
                },
                {
                    "label": "مهندسی محیط زیست",
                    "value": "Environmental Engineering",
                },
                {
                    "label": "مهندسی سازه های دریایی",
                    "value": "Marine Structures Engineering",
                },
            ],
            "School of Computer Engineering": [
                {
                    "label": "مهندسی نرم افزار",
                    "value": "Software Engineering",
                },
                {
                    "label": "هوش مصنوعی و رباتیک",
                    "value": "Artificial Intelligence & Robotics",
                },
                {
                    "label": "معماری سیستم های کامپیوتری",
                    "value": "Computer Systems Architecture",
                },
                {
                    "label": "مهندسی کامپیوتر - شبکه های کامپیوتری",
                    "value": "Computer Engineering - Computer Networks",
                },
            ],
            "School of Electrical Engineering": [
                {
                    "label": "سیستم های ارتباطی",
                    "value": "Communication Systems",
                },
                {
                    "label": "سیستم های قدرت",
                    "value": "Power Systems",
                },
                {
                    "label": "الکترونیک",
                    "value": "Electronics",
                },
                {
                    "label": "سیستمهای کنترل",
                    "value": "Control Systems",
                },
                {
                    "label": "بیو الکتریک",
                    "value": "Bio-Electrics",
                },
                {
                    "label": "میدان های الکترومغناطیسی و امواج",
                    "value": "Electromagnetic Fields and Waves",
                },
            ],
            "School of Industrial Engineering": [
                {
                    "label": "مهندسی فناوری اطلاعات - تجارت الکترونیک",
                    "value": "Information Technology Engineering - Electronic Commerce",
                },
                {
                    "label": "بهینه سازی سیستم",
                    "value": "Systems Optimization",
                },
                {
                    "label": "زنجیره تامین و مهندسی لجستیک",
                    "value": "Supply Chain and Logistic Engineering",
                },
                {
                    "label": "مدیریت مهندسی",
                    "value": "Engineering Management",
                },
                {
                    "label": "سیستم های کلان اجتماعی-اقتصادی",
                    "value": "Socio-Economic Macro Systems",
                },
                {
                    "label": "کیفیت و بهره وری",
                    "value": "Quality & Productivity",
                },
            ],
            "School of Mathematics": [
                {
                    "label": "ریاضیات محض - جبر",
                    "value": "Pure Mathematics - Algebra",
                },
                {
                    "label": "ریاضی محض - هندسه",
                    "value": "Pure Mathematics - Geometry",
                },
                {
                    "label": "ریاضیات محض - تجزیه و تحلیل",
                    "value": "Pure Mathematics - Analysis",
                },
                {
                    "label": "ریاضی کاربردی - تحلیل عددی",
                    "value": "Applied Mathematics - Numerical Analysis",
                },
                {
                    "label": "ریاضیات کاربردی - تحقیق در عملیات",
                    "value": "Applied Mathematics - Operation Research",
                },
                {
                    "label": "ریاضی کاربردی - آمار",
                    "value": "Applied Mathematics - Statistics",
                },
            ],
            "School of Mechanical Engineering": [
                {
                    "label": "مهندسی مکانیک",
                    "value": "Mechanical Engineering",
                },
                {
                    "label": "کنترل دینامیک و لرزش",
                    "value": "Dynamics Control and Vibration",
                },
                {
                    "label": "مکانیک جامدات",
                    "value": "Solid Mechanics",
                },
                {
                    "label": "تبدیل انرژی",
                    "value": "Energy Conversion",
                },
                {
                    "label": "تولید",
                    "value": "Manufacturing",
                },
            ],
            "School of Metallurgy and Materials Engineering": [
                {
                    "label": "مهندسی مواد",
                    "value": "Materials Engineering",
                },
            ],
            "School of Physics": [
                {
                    "label": "فیزیک ماده متراکم",
                    "value": "Condensed Matter Physics",
                },
                {
                    "label": "فیزیک اپتیک لیزر",
                    "value": "Laser Optics Physics",
                },
            ],
            "School of Management Economy and Progress Engineering": [
                {
                    "label": "مدیریت فناوری (MOT) - نوآوری فناوری",
                    "value": "Management of Technology (MOT) - Technological Innovation",
                },
                {
                    "label": "مدیریت سازمان عمومی ایران",
                    "value": "Management of Iranian Public Organization",
                },
                {
                    "label": "سیاست علم فناوری",
                    "value": "Science of Technology Policy",
                },
            ],
            "School of Railway Engineering": [
                {
                    "label": "مهندسی سهام نورد راه آهن",
                    "value": "Railway Rolling Stock Engineering",
                },
                {
                    "label": "مهندسی راه آهن و سازه",
                    "value": "Railway Track and Structures Engineering",
                },
                {
                    "label": "کنترل و سیگنالینگ راه آهن",
                    "value": "Railway Control and Signaling",
                },
            ],
        },
    },
}


class AdminOauthLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        max_length=64,
        required=True,
    )

    def validate(self, attrs):
        response = requests.get(
            "https://its.iust.ac.ir/oauth2/userinfo",
            headers={"Authorization": f"Bearer {attrs['access_token']}"},
        )
        if response.status_code == 200:
            response_json = json.loads(response.content)
            user_obj, created = UserModel.objects.get_or_create(
                username=response_json["username"],
                is_active=True,
                is_staff=True,
            )
            user_obj.sub = response_json["sub"]
            user_obj.picurl = response_json["picture"]
            try:
                user_obj.admin_role = getattr(
                    UserModel.AdminOptions, response_json["usertype"]
                )
            except AttributeError:
                pass
            user_obj.save()

            if created:
                find_school = list(
                    filter(
                        lambda item: item["label"] == response_json["department"],
                        data["Master"]["items"],
                    )
                )
                if len(find_school) > 0:
                    AdminModel.objects.create(
                        user=user_obj,
                        role=AdminModel.AdminRoleOptions.department_member,
                        schools=find_school,
                    )

            user_profile = user_obj.user_profile
            user_profile.first_name = response_json["firstname"]
            user_profile.last_name = response_json["lastname"]
            user_profile.save()

            user_obj.set_last_login()
            user_token = Token.objects.get(user=user_obj)
            return {
                "sub": user_obj.sub,
                "is_superuser": user_obj.is_superuser,
                "is_staff": user_obj.is_staff,
                "username": user_obj.username,
                "picurl": user_obj.picurl,
                "full_name": user_profile.get_full_name(),
                "auth_token": user_token.key,
                "can_issuance_letter": user_obj.can_issuance_letter,
            }
        else:
            raise exceptions.ParseError(BaseErrors.invalid_access_token)
