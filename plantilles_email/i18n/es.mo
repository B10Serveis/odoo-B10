��          �      �       H  E*  I  *  �+  *  �U  *  �  @   �  0   (�  4   Y�  !   ��  "   ��  #   Ӫ  $   ��  R   �  B   o�  :  ��  \)  ��  0)  J�  :)  {�  ;)  �( @   �Q 1   3R 6   eR    �R    �R    �R    �R R   S C   WS          	                       
                               <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px;                                                  border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Order from </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    You have a new order available:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Order number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Amount Ordered: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Order date: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Invoice from </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    You have a new invoice available:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Invoice number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Amount invoiced: 
                                                                    <t t-out="format_amount(object.amount_total_signed, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Invoice date: 
                                                                    <t t-out="format_date(object.date) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Order from </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    You have a new quotation available:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Quotation number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Amount Quoted: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Quotation date: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Proforma from </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    You have a new proforma available:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Proforma number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Amount: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Proforma date: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         Invoice_{{ (object.ref or object.name or '').replace('/','_') }} Order_{{ (object.name or '').replace('/','_') }} Quotation_{{ (object.name or '').replace('/','_') }} Standard - Invoice Email Template Standard - Proforma Email Template Standard - Quotation Email Template Standard - Sale Order Email Template {{ object.company_id.name }} Invoice ref. {{ object.name or object.ref or 'n/a' }} {{ object.company_id.name }} Order ref. {{ object.name or 'n/a' }} Project-Id-Version: Odoo Server 16.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2024-02-23 11:08+0100
Last-Translator: Joan Llimiñana <joan@batista10.cat>
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: 
Language: es
X-Generator: Poedit 2.4.2
 <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px;                                                  border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Pedido de </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Estimado/a 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    Tiene un nuevo pedido disponible:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Pedido: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Cliente: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Importe: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Fecha: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                De acuerdo con el establecido al RGPD, lo informamos que trataremos sus datos personales con el fin de realizar la gestión administrativa, "
contable y fiscal. Los datos proporcionados se conservarán el tiempo exigible por una obligación legal y no serán cedidas a terceros excepto previsión legal exigible, o en su "
caso, previo consentimiento del interesado. Podrá ejercer los siguientes derechos sobre sus datos personales: derecho de acceso, rectificación, supresión, olvido, "
limitación, oposición, portabilidad y a retirar el consentimiento prestado, a la dirección señalada en el presente documento. Además, podrá dirigirse a la autoridad de Control competente "
en materia de Protección de Datos para obtener información adicional o presentar una reclamación.

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Factura de </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Estimado/a 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    Tiene una nueva factura disponible:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Factura: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Cliente: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Importe: 
                                                                    <t t-out="format_amount(object.amount_total_signed, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Fecha: 
                                                                    <t t-out="format_date(object.date) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                De acuerdo con el establecido al RGPD, lo informamos que trataremos sus datos personales con el fin de realizar la gestión administrativa, "
contable y fiscal. Los datos proporcionados se conservarán el tiempo exigible por una obligación legal y no serán cedidas a terceros excepto previsión legal exigible, o en su "
caso, previo consentimiento del interesado. Podrá ejercer los siguientes derechos sobre sus datos personales: derecho de acceso, rectificación, supresión, olvido, "
limitación, oposición, portabilidad y a retirar el consentimiento prestado, a la dirección señalada en el presente documento. Además, podrá dirigirse a la autoridad de Control competente "
en materia de Protección de Datos para obtener información adicional o presentar una reclamación.

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Presupuesto de </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Estimado/a 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    Tiene un nuevo presupuesto disponible:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Presupuesto: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Cliente: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Importe: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Fecha: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                De acuerdo con el establecido al RGPD, lo informamos que trataremos sus datos personales con el fin de realizar la gestión administrativa, "
contable y fiscal. Los datos proporcionados se conservarán el tiempo exigible por una obligación legal y no serán cedidas a terceros excepto previsión legal exigible, o en su "
caso, previo consentimiento del interesado. Podrá ejercer los siguientes derechos sobre sus datos personales: derecho de acceso, rectificación, supresión, olvido, "
limitación, oposición, portabilidad y a retirar el consentimiento prestado, a la dirección señalada en el presente documento. Además, podrá dirigirse a la autoridad de Control competente "
en materia de Protección de Datos para obtener información adicional o presentar una reclamación.

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Proforma de </span>
                                                            <t t-out="object.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Estimado/a 
                                                                <t t-out="object.partner_id.name or object.partner_id.comercial or object.partner_id.parent_id.name or ''">
                                                                </t>
                                                                <br>
                                                                    Tiene una nueva proforma disponible:
                                                                <br>
                                                                <p style="margin-left: 16px">
                                                                    Proforma: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br>
                                                                    Cliente: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Importe: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br>
                                                                    Fecha proforma: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.company_id.name">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="user.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="user.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="user.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ user.email }}" style="text-decoration:none; color: #454748;" t-out="user.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="user.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ user.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="user.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                De acuerdo con el establecido al RGPD, lo informamos que trataremos sus datos personales con el fin de realizar la gestión administrativa, "
contable y fiscal. Los datos proporcionados se conservarán el tiempo exigible por una obligación legal y no serán cedidas a terceros excepto previsión legal exigible, o en su "
caso, previo consentimiento del interesado. Podrá ejercer los siguientes derechos sobre sus datos personales: derecho de acceso, rectificación, supresión, olvido, "
limitación, oposición, portabilidad y a retirar el consentimiento prestado, a la dirección señalada en el presente documento. Además, podrá dirigirse a la autoridad de Control competente "
en materia de Protección de Datos para obtener información adicional o presentar una reclamación.

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         Factura_{{ (object.ref or object.name or '').replace('/','_') }} Pedido_{{ (object.name or '').replace('/','_') }} Presupuesto_{{ (object.name or '').replace('/','_') }} Estandar - Email Factura Estandar - Email Proforma Estandar - Email Presupuesto Estandar - Email Pedido {{ object.company_id.name }} Factura ref. {{ object.name or object.ref or 'n/a' }} {{ object.company_id.name }} Pedido ref. {{ object.name or 'n/a' }} 