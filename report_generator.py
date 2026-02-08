"""
Digital Shadow - Report Generator
PDF rapor oluşturma modülü
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, Any, List
import config
import utils
from io import BytesIO


class ReportGenerator:
    """PDF rapor oluşturucu"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Özel stiller oluştur"""
        
        # Başlık stili
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Alt başlık
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#8b5cf6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Normal metin
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            fontName='Helvetica'
        ))
    
    def generate_analysis_report(self, filename: str, user_data: Dict[str, Any],
                                analysis_data: Dict[str, Any], 
                                chart_images: Dict[str, BytesIO] = None) -> bool:
        """
        Analiz raporu oluştur
        
        Args:
            filename: PDF dosya adı
            user_data: Kullanıcı bilgileri
            analysis_data: Analiz sonuçları
            chart_images: Grafik görselleri (BytesIO dict)
        
        Returns:
            bool: Başarılı mı?
        """
        try:
            # Grafikler yoksa oluştur
            if not chart_images:
                chart_images = self._generate_charts(analysis_data)
            
            # PDF oluştur
            doc = SimpleDocTemplate(
                filename,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # İçerik listesi
            story = []
            
            # Başlık
            story.append(Paragraph(config.REPORT_TITLE, self.styles['CustomTitle']))
            story.append(Spacer(1, 0.5*cm))
            
            # Tarih ve kullanıcı bilgisi
            report_date = datetime.now().strftime("%d.%m.%Y %H:%M")
            story.append(Paragraph(
                f"<b>Rapor Tarihi:</b> {report_date}",
                self.styles['CustomBody']
            ))
            story.append(Paragraph(
                f"<b>Kullanıcı:</b> {user_data.get('username', 'N/A')}",
                self.styles['CustomBody']
            ))
            story.append(Spacer(1, 1*cm))
            
            # Özet Bilgiler
            story.append(Paragraph("📊 Analiz Özeti", self.styles['CustomHeading']))
            
            summary_data = [
                ['Metrik', 'Değer', 'Durum'],
                ['Agresiflik', f"{analysis_data.get('aggression', 0):.2f}", 
                 self._get_status_text(analysis_data.get('aggression', 0))],
                ['Pozitiflik', f"{analysis_data.get('positivity', 0):.2f}",
                 self._get_status_text(analysis_data.get('positivity', 0))],
                ['Risk', f"{analysis_data.get('risk', 0):.2f}",
                 self._get_status_text(analysis_data.get('risk', 0))],
                ['Gizlilik Skoru', f"{analysis_data.get('privacy_score', 0):.1f}",
                 self._get_privacy_status(analysis_data.get('privacy_score', 0))]
            ]
            
            summary_table = Table(summary_data, colWidths=[6*cm, 4*cm, 5*cm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')])
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 1*cm))
            
            # AI Yorumu
            story.append(Paragraph("🤖 AI Değerlendirmesi", self.styles['CustomHeading']))
            ai_comment = analysis_data.get('ai_comment', 'Yorum yok')
            story.append(Paragraph(ai_comment, self.styles['CustomBody']))
            story.append(Spacer(1, 1*cm))
            
            # Dominant Özellik
            dominant = analysis_data.get('dominant_trait', 'unknown')
            dominant_text = self._get_dominant_text(dominant)
            story.append(Paragraph("🎯 Dominant Özellik", self.styles['CustomHeading']))
            story.append(Paragraph(dominant_text, self.styles['CustomBody']))
            story.append(Spacer(1, 1*cm))
            
            # Grafikler (eğer varsa)
            if chart_images:
                story.append(PageBreak())
                story.append(Paragraph("📈 Görsel Analizler", self.styles['CustomHeading']))
                story.append(Spacer(1, 0.5*cm))
                
                for chart_name, img_buffer in chart_images.items():
                    try:
                        img = Image(img_buffer, width=15*cm, height=10*cm)
                        story.append(img)
                        story.append(Spacer(1, 1*cm))
                    except Exception as e:
                        print(f"Chart image error: {e}")
            
            # Öneriler
            story.append(PageBreak())
            story.append(Paragraph("💡 Öneriler", self.styles['CustomHeading']))
            recommendations = self._generate_recommendations(analysis_data)
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
            
            story.append(Spacer(1, 2*cm))
            
            # Footer
            story.append(Paragraph(
                f"<i>Bu rapor {config.APP_NAME} v{config.APP_VERSION} tarafından otomatik oluşturulmuştur.</i>",
                self.styles['CustomBody']
            ))
            
            # PDF'i oluştur
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Report generation error: {e}")
            return False
    
    def _generate_charts(self, analysis_data: Dict[str, Any]) -> Dict[str, BytesIO]:
        """Grafikleri otomatik oluştur"""
        from visualizer import visualizer
        
        charts = {}
        
        try:
            # Skor grafiği
            fig = visualizer.create_score_chart(
                analysis_data.get('aggression', 0),
                analysis_data.get('positivity', 0),
                analysis_data.get('risk', 0),
                analysis_data.get('neutral', 0)
            )
            charts['scores'] = visualizer.fig_to_bytes(fig)
            
            # Radar grafiği
            fig = visualizer.create_radar_chart(
                analysis_data.get('aggression', 0),
                analysis_data.get('positivity', 0),
                analysis_data.get('risk', 0),
                analysis_data.get('privacy_score', 50)
            )
            charts['radar'] = visualizer.fig_to_bytes(fig)
            
        except Exception as e:
            print(f"Chart generation error: {e}")
        
        return charts
    
    def _get_status_text(self, value: float) -> str:
        """Skor durumu metni"""
        if value < 0.3:
            return "Düşük"
        elif value < 0.6:
            return "Orta"
        else:
            return "Yüksek"
    
    def _get_privacy_status(self, score: float) -> str:
        """Gizlilik durumu"""
        if score < 30:
            return "İyi"
        elif score < 60:
            return "Orta"
        else:
            return "Kötü"
    
    def _get_dominant_text(self, dominant: str) -> str:
        """Dominant özellik açıklaması"""
        texts = {
            "aggressive": "Agresif ve çatışmacı bir dijital profil. Sosyal medyada sert bir dil kullanıyorsunuz.",
            "positive": "Pozitif ve yapıcı bir dijital kimlik. İletişiminiz olumlu ve destekleyici.",
            "risk": "Riskli davranış kalıpları. Dijital güvenliğinize daha fazla dikkat etmelisiniz.",
            "neutral": "Nötr ve dengeli bir profil. Standart kullanım kalıpları sergiliyorsunuz."
        }
        return texts.get(dominant, "Belirsiz profil.")
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        aggr = analysis_data.get('aggression', 0)
        pos = analysis_data.get('positivity', 0)
        risk = analysis_data.get('risk', 0)
        privacy = analysis_data.get('privacy_score', 0)
        
        if aggr > 0.6:
            recommendations.append(
                "Agresiflik seviyeniz yüksek. Sosyal medyada daha sakin ve yapıcı bir dil kullanmayı deneyin."
            )
        
        if pos < 0.3:
            recommendations.append(
                "Pozitiflik skorunuz düşük. Daha olumlu ve destekleyici içerikler paylaşabilirsiniz."
            )
        
        if risk > 0.6:
            recommendations.append(
                "Risk seviyeniz yüksek. Kişisel bilgilerinizi paylaşırken daha dikkatli olun."
            )
        
        if privacy > 60:
            recommendations.append(
                "Gizlilik skorunuz kötü durumda. Sosyal medya hesaplarınızın gizlilik ayarlarını gözden geçirin."
            )
        
        if not recommendations:
            recommendations.append(
                "Dijital profiliniz dengeli görünüyor. Mevcut yaklaşımınızı sürdürebilirsiniz."
            )
        
        recommendations.append(
            "Düzenli olarak dijital ayak izinizi kontrol edin ve gereksiz hesapları kapatın."
        )
        
        return recommendations


# Global report generator instance
report_generator = ReportGenerator()
