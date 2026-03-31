export type BillLineItem = {
  id: string
  label: string
  unitPricePaise: number
  quantity: number
}

export type BillAdjustment = {
  id: string
  label: string
  amountPaise: number
  type: 'charge' | 'discount'
}

export type BillPayment = {
  id: string
  label: string
  amountPaise: number
  mode: string
}

export type PatientBill = {
  patientId: string
  invoiceNumber: string
  lineItems: BillLineItem[]
  adjustments: BillAdjustment[]
  payments: BillPayment[]
}

export function formatCurrencyFromPaise(amountPaise: number) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amountPaise / 100)
}

export function calculateBillTotals(bill: PatientBill) {
  const subtotalPaise = bill.lineItems.reduce((sum, item) => sum + item.unitPricePaise * item.quantity, 0)
  const chargeAdjustmentsPaise = bill.adjustments
    .filter((item) => item.type === 'charge')
    .reduce((sum, item) => sum + item.amountPaise, 0)
  const discountPaise = bill.adjustments
    .filter((item) => item.type === 'discount')
    .reduce((sum, item) => sum + item.amountPaise, 0)
  const totalPaise = subtotalPaise + chargeAdjustmentsPaise - discountPaise
  const paidPaise = bill.payments.reduce((sum, item) => sum + item.amountPaise, 0)
  const duePaise = Math.max(totalPaise - paidPaise, 0)
  const creditPaise = Math.max(paidPaise - totalPaise, 0)

  return {
    subtotalPaise,
    chargeAdjustmentsPaise,
    discountPaise,
    totalPaise,
    paidPaise,
    duePaise,
    creditPaise,
  }
}

export function auditBill(bill: PatientBill) {
  const issues: string[] = []
  const totals = calculateBillTotals(bill)

  if (!bill.invoiceNumber.trim()) {
    issues.push('Invoice number is missing.')
  }

  if (bill.lineItems.length === 0) {
    issues.push('Bill has no line items.')
  }

  bill.lineItems.forEach((item) => {
    if (!item.label.trim()) {
      issues.push(`A line item is missing its label.`)
    }

    if (item.quantity <= 0) {
      issues.push(`${item.label || 'A line item'} has an invalid quantity.`)
    }

    if (item.unitPricePaise < 0) {
      issues.push(`${item.label || 'A line item'} has a negative unit price.`)
    }
  })

  bill.adjustments.forEach((item) => {
    if (item.amountPaise < 0) {
      issues.push(`${item.label || 'An adjustment'} has a negative value.`)
    }
  })

  bill.payments.forEach((payment) => {
    if (payment.amountPaise < 0) {
      issues.push(`${payment.label || 'A payment'} has a negative value.`)
    }
  })

  if (totals.totalPaise < 0) {
    issues.push('Bill total cannot be negative.')
  }

  return {
    issues,
    isValid: issues.length === 0,
    totals,
  }
}
