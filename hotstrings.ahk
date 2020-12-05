; Medical abbreviations hotstrings/hotkeys
; Based on Wikipedia (https://en.wikipedia.org/wiki/List_of_abbreviations_used_in_medical_prescriptions) and Pocket Medicine 6th Edition
; Current as of December 5 2020
; -----------------------------------------------------------------------------
; Copyright (c) 2018-2020, Chang-Yi Yen <changyiyen@gmail.com>
; All rights reserved.
;
; Redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions are met:
;    * Redistributions of source code must retain the above copyright
;      notice, this list of conditions and the following disclaimer.
;    * Redistributions in binary form must reproduce the above copyright
;      notice, this list of conditions and the following disclaimer in the
;      documentation and/or other materials provided with the distribution.
;    * Neither the name of the organization nor the
;      names of its contributors may be used to endorse or promote products
;      derived from this software without specific prior written permission.
;
; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
; ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
; WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
; DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
; DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
; (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
; ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
; (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
; SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

; Set hotstrings to be case-sensitive
#Hotstring c

;; Deprecated by Joint Commission
;; https://www.jointcommission.org/facts_about_do_not_use_list/
;::U::units  ; commented out here due to potential triggering if "U/A" (urinalysis) or "U/C" (urine culture) is typed
::IU::international units  ; may be mistaken for "IV" or "10"
::qd::daily  ; quaque die; may be mistaken for "qod"
::q.d.::daily
::QD::daily
::Q.D.::daily
::qod::every other day  ; quaque altera die; may be mistaken for "qd"
::q.o.d::every other day
::QOD::every other day
::Q.O.D.::every other day
; Rule regarding leading and trailing zeros not defined here due to context sensitivity (allowed for non-prescription values)
::MgSO4::magnesium sulfate  ; may be mistaken for morphine sulfate (MSO4)
::MSO4::morphine sulfate  ; may be mistaken for magnesium sulfate (MgSO4)

;; Deprecated by Institute for Safe Medication Practices and American Medical Association
::a.d.::right ear  ; auris dextra; "a" may be mistaken for "o"
::AD::right ear
::a.s.::left ear  ; auris sinistra; "a" may be mistaken for "o"
;::AS::left ear  ; may be confused with aortic stenosis
::a.u.::both ears  ; auris utraque; "a" may be mistaken for "o"
::AU::both ears
::b.i.d.::twice a day  ; bis in die; deprecated by AMA Manual of Style
::BID::twice a day
::B.I.D.::twice a day
::b.d.::twice a day
::b.t.::bedtime  ; may be mistaken for b.i.d.
::c.c.::mL  ; may be confused with "with food" ("cum cibo")
::d.::day  ; may be confused with "dose"
::dc::discontinue  ; may be confused with "discharge"
::d/c::discontinue
::DC::discontinue
::D/C::discontinue
::DTO::deodorized tincture of opium  ; may be confused with "diluted tincture of opium"
::hs::at bedtime  ; hora somni; may be confused with "half-strength"
::h.s.::at bedtime
::HS::at bedtime
::H.S.::at bedtime
::IJ::injection  ; may be mistaken for "IV"
::IN::intranasal  ; may be mistaken for "IM" or "IV"
;::IT::intrathecal  ; may be mistaken for other abbreviations; commented out here due to potential confusion with "information technology"
::npo::nothing by mouth  ; nil per os; deprecated by AMA Manual of Style
::n.p.o.::nothing by mouth
::NPO::nothing by mouth
::N.P.O.::nothing by mouth
::o.d.::right eye  ; oculus dexter; "o" may be mistaken for "a"
::OD::right eye  ; oculus dexter
::o.s.::left eye  ; oculus sinister; "o" may be mistaken for "a"
::OS::left eye  ; oculus sinister
::o.u.::both eyes  ; oculus uterque; "o" may be mistaken for "a"
::OU::both eyes  ; oculus uterque;
::p.o.::by mouth  ; per os; deprecated by AMA Manual of Style
::PO::by mouth
::q.h.s.::every night at bedtime  ; quaque hora somni; may be mistaken for "q.h.r" (every hour)
::q.i.d.::4 times a day  ; quater in die; may be mistaken for "qd" or "qod"; deprecated by AMA Manual of Style
::QID::4 times a day
::q.n.::every night  ; may be mistaken for "qh" (every hour)
::QN::every night
::SC::subcutaneous  ; may be mistaken for "SL" (sublingual)
::s.s.::sliding scale  ; may be mistaken for "55"
::SS::sliding scale
::SSI::sliding scale regular insulin  ; may be confused with "strong solution of iodine" or "SSRI"
::SQ::subcutaneously
::tid::3 times a day  ; ter in die; deprecated by AMA Manual of Style
::t.i.d.::3 times a day
::TID::3 times a day
::T.I.D.::3 times a day
::td::3 times a day  ; ter in die; deprecated by AMA Manual of Style
::t.d.::3 times a day
::TD::3 times a day
::T.D.::3 times a day
::tiw::3 times a week  ; may be mistaken for "twice a week"
::t.i.w.::3 times a week
::TIW::3 times a week
::T.I.W.::3 times a week
::μg::microgram  ; may be mistaken for "milligram" ("mg")
::@::at  ; may be mistaken for "2"
;::>:: greater than  ; may be mistaken for "7" ; commented out here due to potential interference when typing ASCII arrows
;::<:: less than  ; may be mistaken for "L" ; commented out here due to potential interference when typing ASCII arrows

;; Additional abbreviations observed at NCKUH
::AAD::discharge against medical advice
::abd::abdominal
::AMA::against medical advice
::a/w::associated with
::BM::bone marrow
::BS::blood sugar
::BSA::body surface area
::bx::biopsy
::C+A+P::chest + abdomen + pelvis
::CD::change dressings
::c.m.::tomorrow morning  ; cras mane
::C/T::chemotherapy
::ddx::differential diagnoses
::dx::diagnosis
::dz::disease
::F/S::fingerstick glucose
::f/u::follow-up
::gtt::drops  ; gutta/guttae
::hr::hour
::hx::history
::IBW::ideal body weight
::MBD::discharge  ; "may be discharged"
::mcg::microgram  ; may be mistaken for "milligram" ("mg")
::OPD::outpatient clinic
;::PD::peritoneal dialysis
;::PD::disease progression
::R/T::radiotherapy
::RTC::return to clinic
::SOB::shortness of breath
::tx::treatment
::ug::microgram  ; may be mistaken for "milligram" ("mg")
;:?:WM:: with meal  ; commented out here due to potential confusion with "Waldenstrom's macroglobulinemia"
::w/in::within
::WNL::within normal limits
::w/o::without
::w/u::workup
::y/o::{bs 1}-year-old

;; Common drug abbreviations
::5-ASA::mesalazine
::6-MP::6-mercaptopurine
::abx::antibiotics
::ACV::acyclovir  ; as defined in Pocket Medicine
::AMB::amphotericin B  ; as defined in NCKUH Formulary 12e
::ASA::aspirin  ; acetylsalicylic acid
::AZA::azathioprine
::BDZ::benzodiazepine  ; as defined in Pocket Medicine
::BZD::benzodiazepine
::Cftx::ceftriaxone  ; as defined in Pocket Medicine
::CsA::cyclosporine A
::CTX::ceftriaxone
::DA::dopamine
::EPO::erythropoietin
::HCQ::hydroxychloroquine
::IFN::interferon
::INH::isoniazid  ; isonicotinylhydrazide
::MTX::methotrexate
::NTG::nitroglycerin
::PZA::pyrazinamide
::RTX::rituximab
::SSZ::sulfasalazine

;; Change proprietary names to INN
::Aldactone::spironolactone
::Brosym::cefoperazone-sulbactam
::Cravit::levofloxacin
::Dilatrend::carvedilol
::Fluitran::trichlormethiazide
::Forxiga::dapagliflozin
::Herbesser::diltiazem
::Kascoal::dimethicone
::Lasix::furosemide
::Mepem::meropenem
::Nebilet::nebivolol
::Norvasc::amlodipine
::Paramol::acetaminophen
::Plavix::clopidogrel
::Pletaal::cilostazol
::Primperan::metoclopramide
::Takepron::lansoprazole
::Tazocin::piperacillin-tazobactam
::Unasyn::ampicillin-sulbactam
::Weimok::famotidine
::Xyzal::levocetirizine

;; Common procedure/therapy/surgery abbreviations
;::BCS::breast-conserving surgery  ; commented out here due to potential confusion with "biochemistry"
::CAG::coronary angiography
::CAPD::continuous ambulatory peritoneal dialysis
::CPCR::cardiopulmonocerebral resuscitation
::DES::drug-eluting stent
::ECG::electrocardiography
::EKG::electrocardiography
;::EPS::electrophysiological study ; commented out here due to potential confusion with "extrapyramidal symptoms"
::ERBD::endoscopic retrograde biliary drainage
::ERCP::endoscopic retrograde cholangiopancreatography
::ETT::endotracheal intubation
::ICD::implantable cardioverter defibrillator
::iHD::intermittent hemodialysis
::LP::lumbar puncture
::PCI::percutaneous coronary intervention
::POBA::plain-old balloon angioplasty
::POBAS::plain-old balloon angioplasty with stenting
::PPM::permanent pacemaker
::PTA::percutaneous translumenal angioplasty
::PTCD::percutaneous transhepatic cholangial drainage
::PTGBD::percutaneous transhepatic gallbladder drainage
::RFCA::radiofrequency catheter ablation
::S/C::sputum culture
::S/R::sputum routine
::TAVI::transcatheter aortic valve implantation
::TEE::transesophageal echocardiography
::TRH::total radical hysterectomy
::TTM::targeted temperature management
::U/A::urinalysis
::U/C::urine culture
::UCG::transthoracic echocardiography ; used at NTUH

;; Common medical condition abbreviations
::AAA::abdominal aortic aneurysm
::ACKD::acute on chronic kidney disease
::ACOS::asthma-COPD overlap syndrome
::ALL::acute lymphoid leukemia
::AML::acute myeloid leukemia
::AR::aortic regurgitation
::AS::aortic valve stenosis
::BPH::benign prostatic hypertrophy
::CA::cancer
::CAD::coronary artery disease
::CAP::community-acquired pneumonia
;::CD::Crohn's disease  ; commented out here due to potential confusion with "change dressings"
::CHF::congestive heart failure
::COPD::chronic obstructive pulmonary disease
::CRC::colorectal cancer
::DCM::dilated cardiomyopathy
::DLBCL::diffuse large B cell lymphoma
::DM::dermatomyositis
;::DM::diabetes mellitus
::ESRD::end-stage renal disease
::GERD::gastroesophageal reflux disease
::GIB::gastrointestinal bleeding
::GIST::gastrointestinal stromal tumor
::HAP::hospital-acquired pneumonia
::HF::heart failure
::HFpEF::heart failure with preserved ejection fraction
::HFrEF::heart failure with reduced ejection fraction
::HoTN::hypotension
::HTN::hypertension
::IHCA::in-hospital cardiac arrest
::IPNB::intraductal papillary neoplasm of the bile duct
::ISR::in-stent restenosis
::JDM::juvenile dermatomyositis
::LAP::lymphadenopathy
::MI::myocardial infarction
::MM::multiple myeloma
::MR::mitral valve regurgitation
::NTM::nontuberculous mycobacteria
::PEA::pulseless electrical activity
::PNA::pneumonia
::PsA::psoriatic arthritis
::ROSC::return of spontaneous circulation
::SOB::shortness of breath
::SpA::spondyloarthropathy
::SSS::sick sinus syndrome
::TB::tuberculosis
::UC::ulcerative colitis
::UTI::urinary tract infection

;; Common microbiology-related abbreviations
::CoNS::coagulase-negative Streptococci
::CRAB::carbapenem-resistant Acinetobacter baumannii
::CRE::carbapenem-resistant Enterobacteriaceae
::CRKP::carbapenem-resistant Klebsiella pneumoniae
::ESBL::extended-spectrum beta-lactamase
::GNB::gram-negative bacilli
::GPC::gram-negative cocci
::KP::Klebsiella pneumoniae
::MRSA::methicillin-resistant Staphylococcus aureus
::MSSA::methicillin-susceptible Staphylococcus aureus
::NTM::non-tuberculous mycobacteria
::PsA::Pseudomonas aeruginosa
::VRE::vancomycin-resistant Enterococcus

;; Common cardiology-related abbreviations
::1-V-D::one-vessel disease
::2-V-D::two-vessel disease
::3-V-D::three-vessel disease
::AVA::aortic valve area
::ERI::Elective Replacement Interval
::LAA::left atrial appendage
::LAD::left anterior descending artery
::LCx::left circumflex
::LVEF::left ventricle ejection fraction
::RCA::right coronary artery

;; Other medical terms
::BSA::body surface area
::IBW::ideal body weight
::ICA::internal carotid artery
::infxn::infection
::PCT::procalcitonin
