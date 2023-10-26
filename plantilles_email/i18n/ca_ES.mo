��          D      l       �   �!  �      �"  @   �"  R   �"    4#  �!  N$     F  @   /F  R   pF                          <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table style="padding: 16px; background-color: #F1F1F1; color: #454748; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>
                                    <!-- HEADER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle">
                                                            <span style="font-size: 10px;">Your Invoice</span>
                                                            <br/>
                                                            <span style="font-size: 20px; font-weight: bold;" t-out="object.name or 'n/a'" contenteditable="false">
                                                            </span>
                                                        </td>
                                                        <td valign="middle" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="text-align:center;">
                                                            <hr style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin:16px 0px 16px 0px;" width="100%" contenteditable="false"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.user_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                    ,
                                                                <br/>
                                                                    You have a new Invoice available:
                                                                <br/>
                                                                    Inovice number: 
                                                                <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Ammount invoiced: 
                                                                <t t-out="object.amount_total_signed" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Inovice date: 
                                                                <t t-out="object.date or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                <br/>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
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
         Invoice Email Template Invoice_{{ (object.ref or object.name or '').replace('/','_') }} {{ object.company_id.name }} Invoice ref. {{ object.name or object.ref or 'n/a' }} Project-Id-Version: Odoo Server 15.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2023-10-26 11:03+0200
Last-Translator: 
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: 
Language: ca_ES
X-Generator: Poedit 2.4.2
 <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table style="padding: 16px; background-color: #F1F1F1; color: #454748; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>
                                    <!-- HEADER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle">
                                                            <span style="font-size: 10px;">La teva factura</span>
                                                            <br/>
                                                            <span style="font-size: 20px; font-weight: bold;" t-out="object.name or 'n/a'" contenteditable="false">
                                                            </span>
                                                        </td>
                                                        <td valign="middle" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="text-align:center;">
                                                            <hr style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin:16px 0px 16px 0px;" width="100%" contenteditable="false"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px;" valign="top">
                                                            <div>
                                                                <t t-out="object.user_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                    ,
                                                                <br/>
                                                                    Tens una nova factura disponible:
                                                                <br/>
                                                                    Número de factura: 
                                                                <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Import de la factura: 
                                                                <t t-out="object.amount_total_signed" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Data de la factura: 
                                                                <t t-out="object.date or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                <br/>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
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
         Factura - Email Estandard Factura_{{ (object.ref or object.name or '').replace('/','_') }} {{ object.company_id.name }} Factura ref. {{ object.name or object.ref or 'n/a' }} 