#include <qt/transactionoverviewwidget.h>

#include <qt/transactiontablemodel.h>

#include <QListView>
#include <QSize>
#include <QSizePolicy>

TransactionOverviewWidget::TransactionOverviewWidget(QWidget* parent)
    : QListView(parent) {}

QSize TransactionOverviewWidget::sizeHint() const
{
    return {sizeHintForColumn(TransactionTableModel::ToAddress), QListView::sizeHint().height()};
}

void TransactionOverviewWidget::showEvent(QShowEvent* event)
{
    Q_UNUSED(event);
    QSizePolicy sp = sizePolicy();
    sp.setHorizontalPolicy(QSizePolicy::Minimum);
    setSizePolicy(sp);
}
