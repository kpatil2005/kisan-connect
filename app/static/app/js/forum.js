const stateSelect = document.getElementById('state-select');
const districtSelect = document.getElementById('district-select');

const addStateSelect = document.getElementById('state-add');
const addDistrictSelect = document.getElementById('district-add');

function populateDistricts(stateValue, targetSelect) {
    targetSelect.innerHTML = '<option value="">-- Choose District --</option>';
    if (!stateValue) return;

    fetch(`/forum/get_districts/?state=${stateValue}`)
        .then(res => res.json())
        .then(data => {
            data.districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                targetSelect.appendChild(option);
            });
            targetSelect.disabled = false;
        })
        .catch(err => console.error(err));
}

// Search form
stateSelect.addEventListener('change', function () {
    populateDistricts(this.value, districtSelect);
});

// Add group modal form
addStateSelect.addEventListener('change', function () {
    populateDistricts(this.value, addDistrictSelect);
});
